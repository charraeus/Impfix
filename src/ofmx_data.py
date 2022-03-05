"""Read the Open Flightmaps data.

Format of Open Flight Maps File :
(for more details see separate documents)

# Two examples of Dpn knots
#-----------------------------------------------
#
# ... other knots
#
#   <Dpn>
#     <DpnUid mid="3df92f71-c2a6-fbf5-9bba-59f1892329f8" region="LOVV">
#       <codeId>S</codeId>
#       <geoLat>47.33611111N</geoLat>
#       <geoLong>009.62222222E</geoLong>
#     </DpnUid>
#     <AhpUidAssoc mid="6fa88865-b0ea-9241-c73f-77b97bbce29b" region="LOVV">
#       <codeId>LOIH</codeId>
#     </AhpUidAssoc>
#     <codeDatum>WGE</codeDatum>
#     <codeType>VFR-MRP</codeType>
#     <txtName>SIERRA</txtName>
#   </Dpn>
#
# ... other knots
#
#   <Dpn>
#     <DpnUid mid="27b81b2e-083b-a61b-5eda-c78995cc3fce" region="LOVV">
#       <codeId>E</codeId>
#       <geoLat>47.45833333N</geoLat>
#       <geoLong>009.71944444E</geoLong>
#     </DpnUid>
#     <AhpUidAssoc mid="6fa88865-b0ea-9241-c73f-77b97bbce29b" region="LOVV">
#       <codeId>LOIH</codeId>
#     </AhpUidAssoc>
#     <codeDatum>WGE</codeDatum>
#     <codeType>VFR-MRP</codeType>
#     <txtName>ECHO</txtName>
#   </Dpn>
"""

import sys
import xml.etree.ElementTree as ET

import settings

# List of reporting point, sorted by region, airport, reporting point id
class ReportingPointClass(list):
    def __init__(self, rp_data: list) -> None:
        _ofmx_data_line = rp_data

    def __repr__(self) -> str:
        return None

ReportingPointList: list = []

class OFMXFileClass:
    def __init__(self, impfix_settings: settings.SettingsClass) -> None:
        ## Settings
        self.__settings_object: settings.SettingsClass = impfix_settings
        try:
            ## XML/OFMX tree of the OFMX file
            self._xml_tree = ET.parse(self.__settings_object.OFM_file_name)
        except IOError as e:
            errno, strerror = e.args
            print('**I/O error({0}): {1}'.format(errno,strerror))
            print('**File not found: {0}'.format(self.__settings_object.OFM_file_name))
            exit()
        except:
            print('**Unknown error: ', sys.exc_info()[0:2])
            exit()
        ## Root element of the XML/OFMX tree
        self._tree_root = self._xml_tree.getroot()

        #self._airport_dict: dict = {}
        ## Meta data about the OFMX file
        self._OFMX_meta_data: dict = {}

    @property
    def OFMX_meta_data(self) -> dict:
        # Get all attributes of the root element --> dict (key-value pairs)
        self._OFMX_meta_data = self._tree_root.attrib
        # Get the "name" of the root element and store it in dict
        self._OFMX_meta_data['Root-Tag'] = self._tree_root.tag  # --> "OFMX-Snapshot"
        return self._OFMX_meta_data

    def read_and_parse(self) -> None:
        """Read and parse the OFMX file.

        * Open the OFMX file and parse it.
        * Extract the needed data and store in reporting point list.
        """
        # iterate over all Dpn knots
        print('Reading ''Dpn'' knots of OFM file')
        for dpn in self._tree_root.findall('Dpn'):     # --> list of elements
            rp_data: list = []
            # Find the reporting point type within the Dpn knot and 
            # filter by type if necessary
            # Available types: ['VFR-RP', 'VFR-MRP', 'VFR-HELI', 'VFR-GLDR', 'ICAO']
            # @todo implement filter
            if (dpn.find('codeType') is not None) and \
               (dpn.find('codeType').text in ['VFR-RP', 'VFR-MRP', 'VFR-HELI']):
                rp_data.append(dpn.find('codeType').text)   # RP-type
                if dpn.find('AhpUidAssoc/codeId') is not None:
                    rp_data.insert(0, dpn.find('AhpUidAssoc/codeId').text)  # ICAO airport code
                else:
                    rp_data.insert(0, 'n/a ')
                if dpn.find('txtName') is not None:    
                    rp_data.append(dpn.find('txtName').text)   # RP-Name
                else:
                    rp_data.append('n/a')
                # Find the DpnUid element within the Dpn knot and read the data
                dpn_uid = dpn.find('DpnUid')
                if dpn_uid is not None:
                    rp_data.insert(1, dpn_uid.find('codeId').text)    # RP-Id
                    # Coordinates (RP-longitude and RP-latitude): RP-coordinates
                    rp_data.append(self.convert_to_xplane_coord([dpn_uid.find('geoLat').text, 
                                                                 dpn_uid.find('geoLong').text]))
                    rp_data.insert(0, dpn_uid.attrib.get('region'))   # RP-Region
                else:
                    rp_data.insert(1, '')     # RP-Id
                    rp_data.append(['', ''])  # RP coordinates
                    rp_data.insert(0, '')     # RP region

                # Add reporting point data to reporting point list
                ReportingPointList.append(rp_data)
                if self.__settings_object.verbose:
                    print(rp_data)

        ReportingPointList.sort(key=lambda rp_data: self.rp_sortkey(rp_data))

    # Sort reporting point list by region, icao-id and reporting 
    # point id
    def rp_sortkey(self, rp_data: ReportingPointClass) -> str:
        """
        Return the the sort key for the ReportingPoints list
        
        => to get the sortkey of the list in list a dedicated  
            function is used: create the key out of the first three 
            elements of the listelement (which is also a list) in 
            the ReportingPoints list
        """
        # rp_data's first three elements build the sort key
        sk =  ','.join(str(e) for e in rp_data[0:3])
        return sk

    def convert_to_xplane_coord(self, ofmx: list) -> list:
        """
        Convert coordinates to X-Plane 11-usable coordinates
        
        arguments:
            ofmx:   [lat, long] decimal degree coordinates 
                    of ofmx file in a list
        
        returns
            [lat, long] list with coordinates for X-Plane 11
        """
        xplane_coord = []
        # Latitude: if SOUTH then convert to negative value
        if ofmx[0].endswith('S'):
            ofmx[0] = '-' + ofmx[0]
        # cut last character (N, S)
        xplane_coord.append(ofmx[0][0:len(ofmx[0]) - 1])
        # Longitude: if WEST then convert to negative value
        if ofmx[0].endswith('W'):
            ofmx[1] = '-' + ofmx[1]
        # cut last character (W, E)
        xplane_coord.append(ofmx[1][0:len(ofmx[1]) - 1])
        return xplane_coord

    def get_reporting_point(self) -> list:
        """Generator function to return the ofmx data lines

        Yields:
            rp: single reporting point as list with data elements
        """
        for rp in ReportingPointList:
            yield rp
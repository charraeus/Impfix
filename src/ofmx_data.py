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
        ## Airport dictionary with all reporting points per airport
        self._airport_dict = {}

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
               (dpn.find('codeType').text.strip() in ['VFR-RP', 'VFR-MRP', 'VFR-HELI']):
                # store reporting point type
                rp_data.append(dpn.find('codeType').text.strip())
                # store ICAO airport code
                if dpn.find('AhpUidAssoc/codeId') is not None:
                    rp_data.insert(0, dpn.find('AhpUidAssoc/codeId').text.strip())
                else:
                    rp_data.insert(0, 'n/a ')
                # store reporting point name
                if dpn.find('txtName') is not None:
                    rp_data.append(dpn.find('txtName').text.strip())
                else:
                    rp_data.append('n/a')
                # Find the DpnUid element within the Dpn knot and read the data
                dpn_uid = dpn.find('DpnUid')
                if dpn_uid is not None:
                    # store reporting point id
                    rp_data.insert(1, dpn_uid.find('codeId').text.strip())
                    # store coordinates (RP-longitude and RP-latitude)
                    rp_data.append(self.convert_to_xplane_coord([dpn_uid.find('geoLat').text, 
                                                                 dpn_uid.find('geoLong').text]))
                    # reporting point region
                    rp_data.insert(0, dpn_uid.attrib.get('region'))
                else:
                    rp_data.insert(1, '')     # RP-Id
                    rp_data.append(['', ''])  # RP coordinates
                    rp_data.insert(0, '')     # RP region

                # Create a reporting point id which is only five
                # characters long and unique within one airport
                rp_data.append(self.build_rp_name5(rp_data))

                # Add shortened region
                rp_data.append(rp_data[0][0:2])

                # Add reporting point data to reporting point list
                ReportingPointList.append(rp_data)

                #print(self._airport_dict)

                if self.__settings_object.verbose:
                    print(rp_data)

        # Sort reporting point list by region, icao-id and reporting 
        # point id
        ReportingPointList.sort(key=lambda rp_data: self.rp_sortkey(rp_data))

    def rp_sortkey(self, rp_data: list) -> str:
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
        lat, long = ofmx
        if lat.endswith('S'):
            # Latitude: if SOUTH then convert to negative value
            lat = '-' + lat
        if long.endswith('W'):
            # Longitude: if WEST then convert to negative value
            long = '-' + long
        # cut last character (N, S, W, E) and return the coord as list
        return [lat[0:len(lat) - 1], long[0:len(long) - 1]]

    def get_reporting_point(self) -> list:
        """Generator function to return the ofmx data lines

        Yields:
            rp: single reporting point as list with data elements
        """
        for rp in ReportingPointList:
            yield rp

    def build_rp_name5(self, rp_data: list) -> str:
        """
        rename reporting point ids to max len of 5 characters

        X-Plane 11 only allows navigation point designatores with a
        maximum length of five characters. So all reporting point ids
        have to be shortened to max. five characters length.  

        If there are reporting point which id is longer than five
        characters or not unique within one ariport the id must be 
        rebuilt.  
        e.g.  
        The reporting point ids AUTOBAHN-OST and AUTOBAHN-WEST are
        replaced by AB-O and AB-W.  

        Args:
            rp_data (list): all data available about the reporting point

        Returns:
            str: the new reporting point id
        """
        rp_region, rp_airport, rp_id_old, rp_type, rp_name, *other = rp_data
        rp_id_old = rp_id_old.replace('-', ' ')
        rp_id_words = rp_id_old.split()
        rp_id = rp_id_old[:]

        # only keep the last two words
        while len(rp_id_words) > 2:
            del rp_id_words[0]
        #print(f'los gehts: {rp_id_words=}, {rp_id=}')

        # Rule 1:
        # if reporting point like E, N1, N2
        # replace it with the rp name like ECHO, NOVE1, ...
        if len(rp_id_words[0]) <= 2:
            rp_id = rp_id_words[0].strip()
            if len(rp_id) == 1:
                rp_id = rp_name[0:5]
            elif len(rp_id) == 2 \
                    and rp_id[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    #e.g. ECHO 2, NOVEMBER 1
                    rp_id = rp_name[0:4] + rp_name[-1]
            #print(f'Rule 1: {rp_id=}\n')
        else:
            while len(rp_id) > 5:

                # Rule 2:
                # if first word starts with 'AUTOBAHN',
                # replace the string 'AUTOBAHN' by 'AB'
                # e.g.  
                # AUTOBAHN OST  --> AB OST  
                # AUTOBAHN WEST --> AB WEST  
                # AUTBAHNKNOTEN --> ABKNOTEN
                if rp_id_words[0].startswith('AUTOBAHN'):
                    #print(f'    Rule 2: {rp_id_words=}, {rp_id_words[0]=}')
                    rp_id_words[0] = rp_id_words[0].replace('AUTOBAHN', 'AB')
                    #print(f'    Rule 2e: {rp_id_words}, {rp_id_words[0]=}\n')

                # Rule 3:
                # rp_id_old starts with 'ST.' or 'ST. ' or 'ST ',
                # remove this
                elif rp_id_words[0] in ['ST.', 'ST']:
                    del rp_id_words[0]
                
                # Rule 4:
                # rp_id_old ends with 'NORD', 'SÜD', 'WEST', 'OST',  
                #                     'NORWEST', 'NORDOST', 'SÜDWEST'  
                #                      or 'SÜDOST',  
                # replace this by 'N', 'S', 'W', 'O', 'NW', 'NO', 'SW'  
                #                  or 'SO'  
                # e.g.  
                # AB WEST --> AB W  
                # AMSTETTEN WEST --> AMSTETTEN W  
                elif rp_id_words[-1] in ['NORD', 'SÜD', 'WEST', 'OST']:
                    match rp_id_words[-1]:
                        case 'NORD':
                            rp_id_words[-1] = '-N'
                        case 'SÜD':
                            rp_id_words[-1] = '-S'
                        case 'WEST':
                            rp_id_words[-1] = '-W'
                        case 'OST':
                            rp_id_words[-1] = '-O'

                # Rule 5:
                # rp-id has two words:  
                # shorten the first of two remaining words to three
                #     characters;  
                # if the last word has more than one character:  
                #     shorten the first word to three characters
                #     shorten the last word to two characters  
                #     e.g.  
                #     AMSTETTEN W --> AMS W  
                #     AMSTETTEN PARKPLATZ --> AMSPA  
                elif len(rp_id_words) == 2:
                    #print(f'    Rule 5: {rp_id_words=}, {rp_id=}')
                    e0 = min(3, len(rp_id_words[0]))
                    e1 = 5 - e0
                    rp_id = rp_id_words[0][:e0] + rp_id_words[1][:e1]
                    #print(f'    Rule 5e: {rp_id_words=}, {rp_id=}\n')
                
                # Rule 6:
                # the rp_id is still > 5 characters long and the rules
                # above do not apply:
                # shorten the rp-id to max. five characters  
                # e.g.  
                # LORENZEN --> LOREN  
                else:
                    rp_id = rp_id_words[0][:5]

        # eliminate non unique reporting point names (within one airport)
        # and add the reporting point name to airport dictionary
        count = 0
        is_unique_name = False
        if rp_data[1] in self._airport_dict:
            while not is_unique_name:
                if rp_id in self._airport_dict[rp_data[1]]:
                    # reporting point with same name is already existing
                    e = min(4, len(rp_id) - (1 if count > 0 else 0))
                    count += 1
                    rp_id = rp_id[:e] + str(count)
                else:
                    is_unique_name = True
        self.add_reporting_point(rp_data[1], rp_id)
        return rp_id

    def add_reporting_point(self, rp_airport: str, rp_name5: str) -> None:
        """add a reporting point to the airport"""
        if rp_airport in self._airport_dict:
            rp_list = self._airport_dict[rp_airport]
        else:
            rp_list = []
        rp_list.append(rp_name5)
        self._airport_dict[rp_airport] = rp_list

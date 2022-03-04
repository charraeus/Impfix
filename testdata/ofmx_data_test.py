"""OFMX-Daten parsen
"""

import xml.etree.ElementTree as ET

# Root-Eintrag in der Datei (die ersten 2 Zeilen der xml-Datei):
#-------------------------------------------------
# <?xml version="1.0" encoding="utf-8"?>
# <OFMX-Snapshot version="0.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://schema.openflightmaps.org/0.1/OFMX-Snapshot.xsd" effective="2022-02-08T06:26:43" origin="ofmx editor" created="2022-02-08T06:26:43" namespace="210444d1-4576-e92d-0983-4669182a8c04">

# Und hier zwei Beispieleinträge von Dpn-Knoten:
#-----------------------------------------------
#
# ... hier stehen andere Knoten
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
# ... hier stehen andere Knoten
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

rp_list: list = []

# Datei einlesen und Root-Element suchen
tree = ET.parse('/Users/harraeusc/Documents/Projekte/Impfix/testdata/ofmx_lo/isolated/ofmx_lo.ofmx')
root = tree.getroot()
print('---------\nInfos zu "root":')
# "Name" eines Elements holen --> str
print('      tag: ', root.tag)  # --> "OFMX-Snapshot"

# Alle Attribute eines Elements holen --> dict (Wertepaare)
attrib_dict = root.attrib
print('   attrib: ', attrib_dict)
print('  created: ', attrib_dict.get('created'))    # --> "2022-02-08T06:26:43"
print('effective: ', attrib_dict.get('effective'))  # --> "2022-02-08T06:26:43"

# Attribut eines Elements holen --> str
print('  version: ', root.get('version'))   # --> "0.1"

# Dpn-Knoten suchen und Daten ausgeben
print('\n---------------\nDpn-Knoten:')

# Über alle Dpn-Knoten iterieren
for dpn in root.findall('Dpn'):     # --> Liste von Elements
    rp_data = []
    # Innerhalb eines Dpn-Knoten den RP-Typ finden und ggf. filtern
    if (dpn.find('codeType') != None) and \
        (dpn.find('codeType').text in ['VFR-RP', 'VFR-MRP', 'VFR-HELI', 'VFR-GLDR']):
        rp_data.append(dpn.find('codeType').text)      # RP-Type 'VFR-RP', 'VFR-MRP', 'VFR-HELI', 'VFR-GLDR', 'ICAO']
        if dpn.find('AhpUidAssoc/codeId') != None:
            rp_data.append(dpn.find('AhpUidAssoc/codeId').text)
        if dpn.find('txtName') != None:#    
            rp_data.append(dpn.find('txtName').text)   # RP-Name
         # Innerhalb eines Dpn-Knoten das DpnUid-Element finden
        # und die darunter befindlichen Daten lesen 
        dpn_uid = dpn.find('DpnUid')
        if dpn_uid != None:
            rp_data.append(dpn_uid.find('codeId').text)    # RP-Id
            rp_data.append(dpn_uid.find('geoLat').text)    # RP-Pos Latitude
            rp_data.append(dpn_uid.find('geoLong').text)   # RP-Pos Longitude
            rp_data.append(dpn_uid.attrib.get('region'))   # RP-Region
        
        rp_list.append(rp_data)
        print('.', end='')
print('')

# >>> student_tuples = [
# ...     ('john', 'A', 15),
# ...     ('jane', 'B', 12),
# ...     ('dave', 'B', 10),
# ... ]
# >>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
# [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

# rp_list = [
#   ['VFR-MRP', 'LOWW', 'STRASSHOF', 'STRASSHOF', ...],
#   ['VFR-RP', 'LOWL', 'OSCAR', ...],
#   ...
# ]

#print(sorted(rp_list, key=lambda airport: airport[1]))   # --> funktioniert
rp_list.sort(key=lambda airport: airport[1])
print(rp_list)
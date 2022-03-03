# OFMX-Dokumentation (Auszug)
For English translation see below.

## Einführung und Quelle
Erste Anlaufstelle für eine Beschreibung ist https://gitlab.com/openflightmaps/ofmx.  
Im dortigen Wiki sind die einzelnen Datenelemente beschrieben. Auch Teile der folgenden Doku (englischer Text) ist von dort entnommen.

## Dateinamen
Der Dateiname der ofmx-Dateien ist folgendermaßen aufgebaut (Stand Februar 2022):  
> ofmx_\<ICAO-Region Code\>
>
> Beispiele: 
> * *ofmx_ed* für Deutschland-Daten
> * *ofmx_lo* für Österreich-Daten

## VFR (Pflicht-) Meldepunkte / (Mandatory) Reporting Points (MRP)
Für Pflichtmeldepunkte (MRP)wird das Datenelement *Navigational Aid*, und darin das Element *Designated Point (Dpn)* verwendet. Relevant sind die Elemente, die im *\<CodeType\>* "*VFR-MRP*", oder "*VFR-RP*" stehen haben.  
Diese haben im Key *\<AhpUidAssoc\>* die Region sowie den ICAO-Airport-Code des Flughafens, zu dem der Designated Point gehört, hinterlegt.

* Designated points are well defined and named positions on the map.
* Dpn Designated point  
   |  
   +-- Ahp Airport via AhpUidAssoc  

  Nachfolgend drei Beispiele aus einer realen ofmx-Datei:

  ```xml
  <Dpn source="LF|VAC|LFNT|2018-01-04|1">
    <DpnUid region="LF">
      <codeId>NA</codeId>
      <geoLat>49.98708333N</geoLat>
      <geoLong>003.01986111E</geoLong>
    </DpnUid>
    <AhpUidAssoc region="LF">
      <codeId>LFMV</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-MRP</codeType>
    <txtName>ILE DE BARTHELASSE / BARTHELASSE ISLAND</txtName>
    <txtRmk>see VAC</txtRmk>
  </Dpn>
  <Dpn>
    <DpnUid mid="3f1e72df-8180-9b84-b22d-78ecafd1eefc" region="LOVV">
      <codeId>I</codeId>
      <geoLat>47.23611111N</geoLat>
      <geoLong>011.28027778E</geoLong>
    </DpnUid>
    <AhpUidAssoc mid="bde2ff8b-d211-3c65-d8e0-423d248c734a" region="LOVV">
      <codeId>LOWI</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-MRP</codeType>
    <txtName>INDIA</txtName>
  </Dpn>
  <Dpn>
    <DpnUid mid="c1571120-81ff-f261-b172-ec9778490b68" region="LOVV">
      <codeId>W2</codeId>
      <geoLat>47.28638889N</geoLat>
      <geoLong>011.16972222E</geoLong>
    </DpnUid>
    <AhpUidAssoc mid="bde2ff8b-d211-3c65-d8e0-423d248c734a" region="LOVV">
      <codeId>LOWI</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-RP</codeType>
    <txtName>WHISKEY 2</txtName>
  </Dpn>
  ```
* Dpn – Designated point designated point belongs to 
  * @source [X] – Reference to source of data
* DpnUid [M] – Dpn identifier
  * @region [E] [X] – Region this designated point is located in
  * codeId [M] – Coded identification (e.g. five-letter ICAO name or   ICAO   * nationality code plus at least four letters/digits)
  * geoLat [M] – Location latitude
  * geoLong [M] – Location longitude
* AhpUidAssoc – Associated to Airport
* codeDatum [M] – Always WGE (WGS-84)
* codeType [M] – ICAO (codeId is a five-letter ICAO name), ADHP (codeIdis   * airport related name), COORD (codeId is derived fromgeographical   * coordinates), VFR-RP [X] (reporting point), VFR-MRP [X](mandatory   * reporting point), VFR-ENR [X] (en-route reporting point),VFR-GLDR [X]   * (glider reporting point), VFR-HELI [X] (helicopterreporting point), TOWN   * [X], MOUNTAIN-TOP [X], MOUNTAIN-PASS [X] orOTHER (see remarks)
* txtName – Full name
* valElev [X] – Elevation (only used for types MOUNTAIN-TOP and   *MOUNTAIN-PASS)
* uomElev [X] – Unit of valElev: FT (feet) or M (meters)
* valTrueBrg [X] – Geographic bearing (only used for type MOUNTAIN-PASS)
* valMagBrg [X] – Magnetic bearing (only used for type MOUNTAIN-PASS)
* txtRmk [MD] – Remarks

----

English version:  

# OFMX documentation (excerpt) 
## Introduction and Source 
The first point of contact for a description is https://gitlab.com/openflightmaps/ofmx. The individual data elements are described in the wiki there. Parts of the following documentary are also taken from there. 

## File names 
The file name of the ofmx files is structured as follows (as of February 2022): 
> ofmx_\<ICAO region code\> 
>
> examples: 
> * *ofmx_ed* for Germany data 
> * *ofmx_lo* for Austria data 

## VFR (Mandatory) Reporting Points (MRP) 
Mandatory reporting points (MRP) use the data element *Navigational Aid* and the element *Designated Point (Dpn)*. Relevant are the elements that have "*VFR-MRP*", or "*VFR-RP*" stored in in the *\<CodeType\>* element. They have stored the region and the ICAO airport code of the airport to which the designated point belongs in the key *\<AhpUidAssoc\>.

* Designated points are well defined and named positions on the map.
* Dpn Designated point  
   |  
   +-- Ahp Airport via AhpUidAssoc  

  Nachfolgend drei Beispiele aus einer realen ofmx-Datei:

  ```xml
  <Dpn source="LF|VAC|LFNT|2018-01-04|1">
    <DpnUid region="LF">
      <codeId>NA</codeId>
      <geoLat>49.98708333N</geoLat>
      <geoLong>003.01986111E</geoLong>
    </DpnUid>
    <AhpUidAssoc region="LF">
      <codeId>LFMV</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-MRP</codeType>
    <txtName>ILE DE BARTHELASSE / BARTHELASSE ISLAND</txtName>
    <txtRmk>see VAC</txtRmk>
  </Dpn>
  <Dpn>
    <DpnUid mid="3f1e72df-8180-9b84-b22d-78ecafd1eefc" region="LOVV">
      <codeId>I</codeId>
      <geoLat>47.23611111N</geoLat>
      <geoLong>011.28027778E</geoLong>
    </DpnUid>
    <AhpUidAssoc mid="bde2ff8b-d211-3c65-d8e0-423d248c734a" region="LOVV">
      <codeId>LOWI</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-MRP</codeType>
    <txtName>INDIA</txtName>
  </Dpn>
  <Dpn>
    <DpnUid mid="c1571120-81ff-f261-b172-ec9778490b68" region="LOVV">
      <codeId>W2</codeId>
      <geoLat>47.28638889N</geoLat>
      <geoLong>011.16972222E</geoLong>
    </DpnUid>
    <AhpUidAssoc mid="bde2ff8b-d211-3c65-d8e0-423d248c734a" region="LOVV">
      <codeId>LOWI</codeId>
    </AhpUidAssoc>
    <codeDatum>WGE</codeDatum>
    <codeType>VFR-RP</codeType>
    <txtName>WHISKEY 2</txtName>
  </Dpn>
  ```
* Dpn – Designated point designated point belongs to 
  * @source [X] – Reference to source of data
* DpnUid [M] – Dpn identifier
  * @region [E] [X] – Region this designated point is located in
  * codeId [M] – Coded identification (e.g. five-letter ICAO name or   ICAO   * nationality code plus at least four letters/digits)
  * geoLat [M] – Location latitude
  * geoLong [M] – Location longitude
* AhpUidAssoc – Associated to Airport
* codeDatum [M] – Always WGE (WGS-84)
* codeType [M] – ICAO (codeId is a five-letter ICAO name), ADHP (codeIdis   * airport related name), COORD (codeId is derived fromgeographical   * coordinates), VFR-RP [X] (reporting point), VFR-MRP [X](mandatory   * reporting point), VFR-ENR [X] (en-route reporting point),VFR-GLDR [X]   * (glider reporting point), VFR-HELI [X] (helicopterreporting point), TOWN   * [X], MOUNTAIN-TOP [X], MOUNTAIN-PASS [X] orOTHER (see remarks)
* txtName – Full name
* valElev [X] – Elevation (only used for types MOUNTAIN-TOP and   *MOUNTAIN-PASS)
* uomElev [X] – Unit of valElev: FT (feet) or M (meters)
* valTrueBrg [X] – Geographic bearing (only used for type MOUNTAIN-PASS)
* valMagBrg [X] – Magnetic bearing (only used for type MOUNTAIN-PASS)
* txtRmk [MD] – Remarks

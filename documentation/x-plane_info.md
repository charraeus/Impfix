# Informationen zu X-Plane (Stand Februar 2022)

## Dateien und Pfade
* X-Plane-Installationsverzeichnis = X-Plane-Verzeichnis
  * Windows: oft *C:\X-Plane 11* oder ähnlich
  * Mac: ?
  * Linux: ?
* Datei, die userspezifische Ergänzungen der Navigationsdaten enthält
  * Windows: *user_fix.dat*
* Pfad zur *user_fix.dat*
  * Windows: *C:\X-Plane 11\Custom Data\user_fix.dat*
  * Mac: ?
  * Linux: ?

## X-Plane-Spezifikationen
Quelle: https://developer.x-plane.com

Impfix verwendet das Format "*XPNAV1100, 1150 and 1200*", wie auf der X-Plane-Webseite beschrieben. Alle Detais sind ebenfalls auf dieser Webseite beschrieben. Hier nur die wichtigsten Punkte zum Entwickeln.

Dateiformat-Spezifikationen für die verschiedenen Daten:
* X-Plane ab Version 11.50
  * *XPFIX1101: XP FIX1101 Spec*: X-PLANE NAVIGATION DATA FOR FIXES (USER_FIX.DAT & EARTH_FIX.DAT) FILE SPECIFICATION VERSION 1101  
  https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf

* X-Plane ab Version 12.00
  * *XPFIX1200: XP FIX1200 Spec*: X-PLANE NAVIGATION DATA FOR FIXES (USER_FIX.DAT & EARTH_FIX.DAT) FILE SPECIFICATION VERSION 1200  
  https://developer.x-plane.com/wp-content/uploads/2021/09/XP-FIX1200-Spec.pdf

## Aufbau der Datei *user_fix.dat*
### BASIC CONCEPTS
* Latitudes and longitudes are described in a decimal notation (e.g. 20.12345678).
  * A latitude of 50 degrees 30 minutes south would be defined as -50.50000000
* North latitudes and east longitudes are positive. South latitudes and west longitudes are negative.
* Terminal waypoints must specify the airport whose terminal area they belong to
* Enroute waypoints must specify the ICAO region code as per ICAO document No. 7910
* The non-existing country code “ZZ” is used for user-defined waypoints that are not published in the AIP of any country.
* User-defined waypoints with country code “ZZ” must have a globally unique identifier
* User-defined waypoints with country code “ZZ” must not appear in earth_fix.dat, but only in user_fix.dat
* User-defined waypoints can have empty waypoint type, published waypoints must set the waypoint type field

### FILE CHARACTERISTICS
The earth_fix.dat files are plain text files:
* Fields in the data can be separated by one or more white space (space, tab) characters.
* By default, the files are generated so that columns of data are consistently aligned, but this is not required. 

### FILE STRUCTURE
In common with most other X-Plane data file specification, header rows of data define the origin (“I” = Intel byte order or “A” = Motorola byte order) of a particular copy of a file, and define the file specification version. The file specification must include the four-digit AIRAC cycle date (e.g. 1602 for the AIRAC cycle effective 4-Feb-16, refer to https://www.nm.eurocontrol.int/RAD/common/airac_dates.html for cycle dates), an 8-digit build date and the reference to this document. A copyright message may be added, while the total length of this line is not to exceed 1024 characters:
```
I
1101 Version - data cycle 1602, build 20160204, metadata FixXP1100. Copyright © 2016, Robin A. Peel (robin@xsquawkbox.net)...
```
Subsequent rows of data define each waypoint. Sequence is not important, but by default this file is sorted alphabetically by fix name. The file is terminated by a ‘99’:
```
99
```

### DEFINITION OF DATA FIELDS
Here is example data for a fixes:
```
46.646819444  -123.72238888  AAYRR KSEA K1 4530263
37.770908333  -122.08281111  AAAME ENRT K2 4530263

47.40527778     11.79777778  PWIM1  LOWI  LO
47.29833333     11.66583333  PWIM2  LOWI  LO
47.24027778     11.41833333  PWIM3  LOWI  LO
```

Each column in each row is defined below, using the example data from shown above. 

|Row    | Meaning<br>Example Value         | Explanation              | Valid values    |
|-------|-----------------|-------------------------------------------|-----------------|
|[none] | Fix             | Fix or IFR intersection                   | No row codes are used, since all data refers to fixes |
|       |     46.64641944 | Latitude of fix in decimal degrees        | Eight decimal places supported |
|       |   -123.72238889 | Longitude of fix in decimal degrees       | Eight decimal places supported |
|       |           AAYRR | ID of fix                                 | Usually five characters. Unique within an ICAO region. |
|       |            KSEA | ID of airport terminal area or “ENRT” for enroute fixes | Must be either airport identifier or “ENRT” |
|       |              K1 | ICAO region code of enroute fix or terminal area airport | Must be region code according to ICAO document No. 7910 For terminal waypoints, the region code of the airport is used |
|       |         4530263 | Waypoint type as defined by the 3 columns of ARINC 424.18 field definition 5.42 | 32bit representation of the 3-byte field defined by ARINC 424.18 field type definition 5.42, with the 4th byte set to 0 in Little Endian byte order. This field can be empty ONLY for user waypoints in user_fix.dat |


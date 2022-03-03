# Anforderungen an Impfix

## Einführung

Impfix steht für "**Im**portiere Openflightmap-**Pf**lichtmeldepunkte **i**n **X**-Plane". [open flightmaps Association (OFMA)](https://www.openflightmaps.org) stellt kostenlose, relative aktuelle, Daten über Lufträume zur Verfügung.  
Diese Software dient zum Auslesen von Daten über Pflichtmeldepunkte und zum Generieren einer entsprechenden users.dat-Datei, so dass diese Pflichtmeldepunkte künftig in X-Plane verfügbar sind (z.B. im Garmin 450).

## Ein- und Ausgabedaten

Die Datenbasis wird von der [open flightmaps Association (OFMA)](https://www.openflightmaps.org) zur Verfügung gestellt. Die Datendateien können dort heruntergeladen werden. Als Input wird die Datei im Format OFMX (XML-Format) verwendet.

Als Ausgabedatei dient die Datei ```$X-Plane/Custom Data/user_fix.dat```.  

Beschreibung der Daten:

* Beschreibung der XML-Dateien (XSD): auf [GitLab openflightmaps](https://gitlab.com/openflightmaps/ofmx/-/tree/master/schema_base/4.5-r2)
* Quelle der XML-Daten-Dateien: auf [GitLab openflightmaps](https://www.openflightmaps.org)
* Dateiformat für die ```user_fix.dat```:
  * [X-Plane Developers-Seite](https://developer.x-plane.com/article/navdata-in-x-plane-11/)
  * [XPIX1101 Spec](http://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf)

## Anforderungen

### Anforderungen mit Priorität A

1. Lauffähig auf Plattform Mac OS Catalina und höher (10.5.6).
1. Bedienung über die Kommandozeile.
1. Einlesen der Daten der Pflichtmeldepunkte aus der Datei  
   ```ofmx_<rr>/isolated/ofmx_<rr>_ofmShapeExtension.xml```.  
   ```<rr>``` muss durch die Region gem. ICAO ersetzt werden, also z.B. "ED" für Deutschland.

   Benötigte Daten Pflichtmeldepunkte:
   1. ICAO-Airport-Identifier (z.B. EDDM).
   1. ICAO-Region-Code gemäß ICAO-Dokuments 7910).  
      Für Terminal-Wegpunkte wird der Region-Code des Airports genutzt.
   1. Name des Pflichtmeldepunkts (i.d.R. maximal 5 Zeichen lang).
   1. Koordinaten des Pflichtmeldepunkts
1. Die Daten so umformen und die Datei ```$X-Plane/Custom Data/user_fix.dat``` schreiben, dass sie für die X-Plane-Navigation sowie zur Anzeige in den GNS-/GPS-Geräten in X-Plane genutzt werden können.
1. Die Pflichtmeldepunkte so (um-) benennen, dass sie eindeutig sind (ist evtl. aufgrund des Region-Codes nicht notwendig?).

   Eindeutiges Namensschema für Pflichtmeldepunkte:
   * Maximal fünf (5) Buchstaben oder Ziffern lang.
   * P - Kennzeichen für "Pflichtmeldepunkt".
   * \<AA> - Die letzten 2 Zeichen des ICAO-Codes des Airports.
   * \<xx> - Maximal zwei weitere Buchstaben oder Ziffern zur Benennung des Pflichtmeldepunkts.

   z.B. PWSHA - Pflichtmeldpunkt "Hallein" in LOWS (Salzburg).  
   z.B. PDME1 - Pflichtmeldepunkt "ECHO1" in EDDM (München).
1. Für Laien verständliche Fehler- und Erfolgsmeldungen.
1. Ein- und Ausgabedateiname und Pfad kann per Kommandozeilenoption angegeben werden. Bei Fehlen der Angaben werden die Dateien im aktuellen Verzeichnis des Anwenders gesucht und geschrieben.

### Anforderungen mit Priorität B

1. Automatisches Herunterladen der Eingabedatei von <https://openflightmaps.org>.
1. Einlesen der Daten der Terminal Areas, Restricted Areas etc. aus der Datei ```ofmx_<rr>/isolated/ofmx_<rr>_ofmShapeExtension.xml```.  
   ```<rr>``` muss durch die Region gem. ICAO ersetzt werden, also z.B. "ED" für Deutschland.
1. Möglichkeit, eine bestehende ```$X-Plane/Custom Data/user_fix.dat```-Datei ergänzen. Dabei müssen die bisherigen, generierten Daten gelöscht und durch die aktuellen Daten ersetzt werden.
1. Möglichkeit, nur Pflichtmeldepunkte bzw. Terminal-Area etc. eines bestimmten Airports laden.
1. Lauffähig auf Plattform Windows 64 (Windows 10, Edition 202002 oder höher).
1. Bedienung über ein GUI.

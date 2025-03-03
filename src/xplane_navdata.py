"""
Create and write new user_fix.dat file.

* Copy all none-Impfix-generated data into the new file
* Delete the old data generated by Impfix, according to the 
  start and end marks
* Generate new start, end and end-of-file marks
* Write the requested Open Flight Maps data into the new file
* Backup the old user_fix.dat file
"""

import sys
from datetime import datetime

from ofmx_data import OFMXFileClass
from settings import SettingsClass

class XPlaneNavDataClass:
    ## Nach dieser Marke beginnen die von Impfix erzeugten Daten
    ## Start mark string: All data after this mark is generated
    ## by Impfix
    __ImpfixStartMark: str = ';- DO NOT EDIT BELOW THIS LINE! --Start Impfix-ofmx-data:'
    ## End mark string: All data after this mark is not generated 
    ## by Impfix
    __ImpfixEndMark: str = ';- DO NOT EDIT ABOVE THIS LINE! --End Impfix-ofmx-data:'

    def __init__(self, impfix_settings: SettingsClass) -> None:
        ## Settings information
        self.__settings_: SettingsClass = impfix_settings
        ## File object for existing user_fix.dat file
        self._xplane_user_fix_dat_file = \
            self._open_user_fix_dat_file(impfix_settings.xplane_user_fix_dat_filename)
        ## File object for new user_fix.dat.impfix file
        self._new_user_fix_dat_file = \
            self._create_new_user_fix_dat_file(impfix_settings.new_user_fix_dat_filename)

    def _create_new_user_fix_dat_file(self, filename):
        """Create the **new** user_fix.dat file

        Create new user_fix.dat file as 'user_fix.dat.impfix'. An 
        existing user_fix.dat.impfix file will be overwritten
        without warning.
        """
        try:
            return open(filename, 'w')
        except IOError as e:
            errno, strerror = e.args
            print('**I/O error({}): {}'.format(errno, strerror))
            print('**Error while creating the file \'{}\''.format(filename))
            exit()
        except:
            print('**Unknown error:\n', sys.exc_info()[0:2])
            exit()

    def _open_user_fix_dat_file(self, filename):
        """Open the **existing** user_fix.dat file"""
        try:
            return open(str(filename), 'r')
        except IOError as e:
            errno, strerror = e.args
            print('**I/O error({0}): {1}'.format(errno,strerror))
            print('**File not found: {0}'
                .format(self.__settings_.xplane_user_fix_dat_filename))
            exit()
        except:
            print('**Unknown error:\n', sys.exc_info()[0:2])
            exit()


    def write_new_user_fix_dat_file(self, ofmx_data: OFMXFileClass) -> None:
        """
        Create new user_fix.dat file. 

        1. Copy all none-Impfix-generated data into the new file:
             => copy all lines until the start mark is found.
        2. Generate and write new start mark into the new user_fix.dat
           file.
        3. Write the Open Flight Map data into the new user_fix.dat 
           file.
        4. Generate the new end mark and copy the rest of the old 
           user_fix.dat file.
        5. If necessary write the X-Plane end-of-file mark into 
           the new user_fix.dat file.
        """

        xplane_userfix_dat_eof: str = '99'  # @todo noch in settings aufnehmen
        eof_mark_found: bool = False
        end_mark_found: bool = False
        start_mark_found: bool = False
        ofm_data_written: bool = False

        # Copy data from old into new user_fix.dat file and insert ofmx-data lines
        cur_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%s')
        print('Copying old non-impfix data into new file ', end='')
        for userfix_dat_line in self._xplane_user_fix_dat_file:
            if (not start_mark_found) \
               and (userfix_dat_line.startswith(self.__ImpfixStartMark)):
                # Start mark found => => skip all lines until the end mark
                # Start mark (Begin of Impfix generated data) found 
                #   => do not copy the lines until the end mark into 
                #      the new user_fix.dat file
                start_mark_found = True
            elif userfix_dat_line.startswith(self.__ImpfixEndMark):
                # End mark (End of Impfix generated data) found
                end_mark_found = True
            elif userfix_dat_line.startswith(xplane_userfix_dat_eof):
                # X-Plane end-of-file mark found
                eof_mark_found = True
            if (start_mark_found or eof_mark_found) and (not ofm_data_written):
                # Write new start mark
                self._new_user_fix_dat_file.write(self.__ImpfixStartMark 
                        + 'XXXX' + ' ' + cur_datetime + '\n')
                self._new_user_fix_dat_file.write('; '
                    'effective: {}\n'.format(ofmx_data.OFMX_meta_data.get('effective')))
                # get and write OFMX data
                reporting_point = ofmx_data.get_reporting_point()
                try:
                    if self.__settings_.verbose:
                        print('\nWriting new OFM data\n', end='')
                    while True:
                        # get the data
                        rp_region, rp_airport, rp_id, *other, coords, rp_id5, rp_region2 = next(reporting_point)
                        lat, long = coords
                        # build the line to be written
                        self._new_user_fix_dat_file.write('\t{}\t{}'.format(lat, long))
                        self._new_user_fix_dat_file.write('\t{}'.format(rp_id5))
                        self._new_user_fix_dat_file.write('\t\t{}'.format(rp_airport))
                        self._new_user_fix_dat_file.write('\t{}'.format(rp_region2))
                        self._new_user_fix_dat_file.write('\n')
                        if self.__settings_.verbose:
                            print(rp_region, rp_airport, rp_id, '-->', rp_id5)

                except StopIteration:
                    ofm_data_written = True
                except:
                    print('**Unexpected error:\n', sys.exc_info()[0:2])
                    exit()
                # Write new end mark
                self._new_user_fix_dat_file.write(self.__ImpfixEndMark 
                        + 'XXXX' + ' ' + cur_datetime + '\n')
                print('\nOFM data successfully written\nCopying rest of original file ', end='')

            # Copy lines of the old user_fix.dat file into the new one,
            # but do not copy the lines with the start and end marks,
            # and do not copy all the lines between the start and end mark lines
            if (not start_mark_found) or eof_mark_found:
                self._new_user_fix_dat_file.write(userfix_dat_line)
            if self.__settings_.verbose:
                print('.', end='')

        if not eof_mark_found:
            # No end-of-file mark found (should not occur, but who knows...)
            # Just add the end-of-file mark
            self._new_user_fix_dat_file.write(xplane_userfix_dat_eof + '\n')
            print('**Warning: Missing End-of-File mark.\n... added.')

        # Close files
        self._new_user_fix_dat_file.close()
        self._xplane_user_fix_dat_file.close()
        print('\nNew File successfully created and written')


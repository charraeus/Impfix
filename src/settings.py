"""
Set all needed environment data, parse command line and store
command line data.

* Impfix version and hello information
* Operating system platform and directory separation char
* Command line parameters
"""

import sys, argparse

class SettingsClass:
    """Set all needed environment data, parse command line and store
    command line data.

    * Impfix version and hello information
    * Operating system platform and directory separation char
    * Command line parameters
    """
    ## Impfix version as string - has to be set manually by developer
    impfix_version = '0.1.1'
    ## Impfix hello message part 1
    __cls_impfix_hello_1: str = 'Impfix '
    ## Impfix hello message part 2
    __cls_impfix_hello_2: str = 'Add Open Flight Maps data to X-Plane.\n'
    ## Name extension for new user_fix.dat file
    __cls_new_name_ext: str = '.impfix'

    def __init__(self):
        """Initialise data attributes and parse command line."""        
        # Attributes
        ## Complete Impfix Hello message
        self.impfix_hello = self.__cls_impfix_hello_1 + self.impfix_version \
                        + ' - ' + self.__cls_impfix_hello_2
        ## Verbose Output during execution
        self.verbose: bool = False
        ## Filename of Open Flight Map file inkluding path
        self.OFM_file_name = ''
        ## Filter by reporting point type
        self.filter_by_rp_type = []
        ## Filter by airport's ICAO id
        self.filter_by_airport_icao_id = ''
        ## URL of the Open Flight Maps file
        self.OFM_file_url = ''
        ## Directory separation character
        self.dir_separator = ''
        ## Path and name of X-Plane directory
        self.__xplane_path = ''
        ## Path below X-Plane path and name of X-Plane user_fix.dat
        self.__xplane_user_fix_dat_subdirectory = ''
        ## Full path and name of X-Planeuser_fix.dat
        self.xplane_user_fix_dat_filename = ''

        # Determine operating system platform and set OS dependend 
        # attributes:
        #   System           platform value in impfix_os
        #   ================ ===========================
        #   AIX              'aix'
        #   FreeBSD          'freebsd'
        #   Linux            'linux'
        #   Windows          'win32'
        #   Windows/Cygwin   'cygwin'
        #   macOS            'darwin'
        self.impfix_os = sys.platform
        if self.impfix_os == 'win32':
            # OS is Windows => directory separation char is '\'
            # Two \ are needed because of masking functionality of 
            # the python interpreter
            self.dir_separator = '\\'
            self.__xplane_path = 'C:\\X-Plane 11'
            self.__xplane_user_fix_dat_subdirectory = 'Custom Data\\user_fix.dat'
        else:
            # OS is non-Windows => directory separation char = '/'
            self.impfix_os = 'unix'
            self.dir_separator = '/'
            self.__xplane_path = '/Application/X-Plane 11'
            self.__xplane_user_fix_dat_subdirectory = 'Custom Data/user_fix.dat'
        
        # Parse the command line and set attribute values from command
        # line parameters
        self._parse_command_line()

        # Set path and filename of X-Plane user_fix.dat
        # e.g.   xplane_path = 'c:/x-plane 11'
        #        xplane_user_fix_dat_filename = 'Custom Data/user_fix.dat'
        #           ==> return 'c:/xplane 11/Custom Data/user_fix.dat'
        self.xplane_user_fix_dat_filename = \
           self._create_path_and_filename(self.__xplane_path, 
                                          self.__xplane_user_fix_dat_subdirectory)
        # Set path and filename of new user_fix.dat file
        self.new_user_fix_dat_filename = \
            self.xplane_user_fix_dat_filename + self.__cls_new_name_ext

    def _create_path_and_filename(self, xplane_path: str, sub_path: str) -> str:
        """Erzeugt aus xplane_path, xplane_userdat_path den neuen Dateinamen.
        Außerdem werden die Attribute self.__DirSeparator"""
        # Create filename of the new user_fix.dat file. Ensure the 
        # correct path: Only one (1) directory separation character
        # between xplane_path and xplane_user_dat_path
        if (not xplane_path.endswith(self.dir_separator)) \
            and (not sub_path.startswith(self.dir_separator)):
            # Fall 1: Weder endet XPlanePath mit /, noch beginnt XPlaneUserDatPath mit /
            #         => Verzeichnis-Trennzeichen notwendig
            return xplane_path + self.dir_separator + sub_path
        elif xplane_path.endswith(self.dir_separator) and sub_path.startswith(self.dir_separator):
            # Fall 2: XPlanePath endet mit / und XPlaneUserDatPath startet mit /
            #         => Das letzte Verzeichnstrennzeichen von XPlanePath löschen
            xplane_path = xplane_path.removesuffix(self.dir_separator)
            return xplane_path + sub_path
        else:
            # Fall 3: Entweder endet XPlanePath mit /, oder XPlaneUserDat beginnt mit /
            #         => kein Verzeichnis-Trennzeichen notwendig
            return xplane_path + sub_path


    def _parse_command_line(self):
        """Parse command line und store parameters in attributes.

        usage: Impfix [-h] [-v] [--data {MRP}] [--icao ICAO] 
                      [--xplanepath XPLANEPATH] [-vv] ofmfile

        Add Open Flightmap data to X-Plane.

        positional arguments:
        ofmfile               OpenFlightMap file

        options:
        -h, --help            show this help message and exit
        -v, --version         Print version and exit
        --data {MRP}          filter by reporting point type (MRP, RP, ICAO)
        --icao ICAO           filter by airport's ICAO code
        --xplanepath XPLANEPATH
                                path to X-Plane directory
        -vv, --verbose        show verbose output

        GitLab: https://gitlab.com/charraeus/impfix
        """
        parser = argparse.ArgumentParser(
            description=self.__cls_impfix_hello_2,
            prog='Impfix',
            epilog='GitLab: https://gitlab.com/charraeus/impfix')
        parser.add_argument('-v', '--version', 
            help='Print version and exit',
            action='version', version='%(prog)s Version ' + self.impfix_version)
        parser.add_argument('ofmfile', help='OpenFlightMap file')
        parser.add_argument('--data', 
            help='filter by reporting point type (MRP, RP, ICAO)', 
            choices=['MRP'],
            required=False)     ##!< @todo Sobald andere Daten als MRPs gewählt werden
                                ##!< können, auf True setzen
        parser.add_argument('--icao', 
            help='filter by airport\'s ICAO code')
        #parser.add_argument('--ofmurl', help='URL for download of Open Flight Maps data')
        parser.add_argument('--xplanepath', help='path to X-Plane directory')
        parser.add_argument('-vv', '--verbose', 
            help='show verbose output',
            action='store_true')
        args = parser.parse_args()  
        self.OFM_file_name = args.ofmfile
        self.filter_by_rp_type = args.data
        self.filter_by_airport_icao_id = args.icao
        # if args.ofmurl != None:                   @todo Kommentar entfernen
        #     self.OFM_file_url = args.ofmurl       @todo Kommentar entfernen
        if args.xplanepath != None:
            self.__xplane_path = args.xplanepath
        if args.verbose != None:
            self.verbose = args.verbose

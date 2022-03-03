#!python
"""Impfix main. Add Open Flight Maps data to X-Plane."""

from settings import SettingsClass
from xplane_navdata import XPlaneNavDataClass
from ofmx_data import OFMXFileClass

settings = SettingsClass()
print(settings.impfix_hello)
ofmxdata = OFMXFileClass(settings)
ofmxdata.read_and_parse()
navdata = XPlaneNavDataClass(settings)
navdata.write_new_user_fix_dat_file(ofmxdata)

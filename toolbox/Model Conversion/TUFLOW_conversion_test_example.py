# Here is an example/test script that will see how well the function in TUFLOW_conversion_functions.py
# work and give an example as to how they work

# loading modules:
import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona
import math
import copy
from TUFLOW_conversion_functions import *

# import floodmodeller_api  # imports the full package
from floodmodeller_api import DAT, ZZN, IEF, IED, XML2D  # imports individual classes (recommended)



sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

#load in the test TUFLOW data

tgc_filepath = pathlib.Path('C:/Users/phillio/OneDrive - Jacobs/Documents/TUFLOW_examples/Bootle/Bootle/TUFLOW/Model/BOOT_023.tgc')
tgc_folder_path = tgc_filepath.parent
# give direction to FM folder where new data will be stored.
FM_folder_path = pathlib.Path(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle_FM\Bootle_2D_data")
FM_folder_name = FM_folder_path.name
domain_name = "Domain 1"

# loading empty(ish) xml2d file
# empty_xml = r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle_FM\xml2d_bootle_test.xml"
xml2d = XML2D()

xml2d.domains[domain_name]["computational_area"] = {
    'xll': ...,
    'yll': ...,
    'dx' : ...,
    'nrows' : ...,
    'ncols' : ...,
    'active_area': ...,
    'rotation': ...,
}
TUFLOW_data = convert_tgc_to_list(tgc_filepath)
xll, yll, dx, nrows, ncols, active_area_path_FM, rotation = find_active_area_from_tgc_file(TUFLOW_data, tgc_filepath, FM_folder_path)

xml2d = load_active_area_to_xml( xml2d, xll, yll, dx, nrows, ncols, active_area_path_FM, rotation, FM_folder_name, domain_name)

xml2d = find_and_load_asc_to_xml(xml2d, TUFLOW_data, tgc_folder_path, FM_folder_path, domain_name)

xml2d = find_and_copy_roughness_to_FM_repo(xml2d, TUFLOW_data, tgc_folder_path, FM_folder_path, domain_name)

# change the time given
xml2d.domains["Domain 1"]["time"]["total"] = 1.00

xml2d._write()

save_name = 'Bootle_test_API_only.xml'
xml2d.save(pathlib.Path(FM_folder_path.parent, save_name))




# run
xml2d.simulate()
# re-run starting with blank xml file



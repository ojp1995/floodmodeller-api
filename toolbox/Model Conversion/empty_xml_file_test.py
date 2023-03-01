# this script will test to make sure that the new ""minimum" xml file needed to pass the validation

import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona
import math
import copy

sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")
# import floodmodeller_api  # imports the full package
from floodmodeller_api import DAT, ZZN, IEF, IED, XML2D  # imports individual classes (recommended)


xml2d_file_path = r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle_FM\xml2d_empty_pass_val.xml"
xml2d = XML2D(xml2d_file_path)

xml2d._validate()
# in this file we will be attempting to reading in a TUFLOW .tcf file and convert to a xml2d file
# Looking at the Bootle flood case
import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona

pathlib.Path.cwd()
sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

from floodmodeller_api import XML2D

# open blank 2d xml file
xml = XML2D(r"C:\Users\phillio\Github\xml_2d_test_data\Bootle\2d_simulation_blank.xml")

### old method, not needed anymore
#importing the TUFLOW data as a text file
# TUFLOW_data = open(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Runs\BOOT_~e1~_~s1~_~s2~_~s3~_023.tcf")
#TODO: Replace with try except 
# with open(
# r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Runs\BOOT_~e1~_~s1~_~s2~_~s3~_023.tcf",
#     'rb', 0) as file, \
#         mmap.mmap(file.fileno(), 0, access = mmap.ACCESS_READ) as s:
#     if s.find(b'.tgc') != -1:
#         test_tgc_present = 'true'

# if test_tgc_present == 'true':
#     # now we need to find this and read it in!
#     os.chdir(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model")
#     for file in glob.glob("*.tgc"):
#         tgc_file_name = file
#         print(tgc_file_name)
#         # tgc_filepath = sys.path(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model\tgc_file_name") S
#         tgc_file_path = os.path.join(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model", file)
#         tgc_file = open(os.path.join(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model", file))

# else:
#     raise Exception('.tgc file not found')

# TODO:
# Now we want to interogate the tgc file to pick out information
# Info we want: [xll, yll, dx, nrows, ncols, active_area, rotation]
# x11, yll - > lower left coordinates of box
# dx - > spacial component
# nrows, ncols- > number of rows and columns
# active_area - > as a .shp file, should be able to pull this out relatively easily
# rotation -> challenge, rotation between north south and the line we are using. 
#
# TODO:
# We can isolate dx, nrows and ncols from the raw .tgc file
# target_variables = ['Grid Size (X,Y)', 'Cell Size']


# # Now we will be looking at use geopandas to pul other information  out

# gdf_L015_file_name = gpd.read_file("C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model\gis\2d_loc_BOOT_L_015.shp")
# # gdf_L015_path_name = gpd.datasets.get_path("2d_loc_BOOT_L_015.shp")
# gdf_L015_file = open(gdf_L015_file_name)
# gdf_L015 = gpd.read_file(gdf_L015_file)

# gdf_L015

## new style

# first we want to load the .tgc file
print(pathlib.Path.cwd())
tgcfile = pathlib.Path('C:/Users/phillio/OneDrive - Jacobs/Documents/TUFLOW_examples/Bootle/Bootle/TUFLOW/Model/BOOT_023.tgc')
tgcfile.open('a')

# Not sure this will work - > I don't know how to read this information as variables could be longer/shorter
# there must be an argument to know how many spcaes it is separated by then are we expecting a number or something
# but currently I can't figure that out.
# TODO:
# We can isolate dx, nrows and ncols from the raw .tgc file
# target_variables = ['Grid Size (X,Y)', 'Cell Size']
# output_var = ['xllyll', 'dx']
# for var in range(target_variables):
#     var_str = str(target_variables[var])
#     with tgcfile as file, \
#         mmap.mmap(file.fileno(), 0, access = mmap.ACCESS_READ) as s:
#         if s.find(b'{var_str}'):
#             output_Var[var] = var_str  # this will give the wrong output, we want what is to the right of the equals in the tgc file!

# Can we get this informationtion from the geopandas
try:
    BOOT_L_015_file = pathlib.Path('C:/Users/phillio/OneDrive - Jacobs/Documents/TUFLOW_examples/Bootle/Bootle/TUFLOW/Model/gis/2d_loc_BOOT_L_015.shp')
    BOOT_L_015_file.open('a')
    df_BOOT_L_015 = gpd.read_file(BOOT_L_015_file)
except Exception as e:
    print(e)

df_BOOT_L_015.info()

df_BOOT_L_015.describe()





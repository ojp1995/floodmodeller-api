# in this file we will be attempting to reading in a TUFLOW .tcf file and convert to a xml2d file
# Looking at the Bootle flood case

import sys, mmap, glob, os

sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

from floodmodeller_api import XML2D

# open blank 2d xml file
xml = XML2D(r"C:\Users\phillio\Github\xml_2d_test_data\Bootle\2d_simulation_blank.xml")

#importing the TUFLOW data as a text file
# TUFLOW_data = open(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Runs\BOOT_~e1~_~s1~_~s2~_~s3~_023.tcf")
#TODO: Replace with try except 
with open(
r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Runs\BOOT_~e1~_~s1~_~s2~_~s3~_023.tcf",
    'rb', 0) as file, \
        mmap.mmap(file.fileno(), 0, access = mmap.ACCESS_READ) as s:
    if s.find(b'.tgc') != -1:
        test_tgc_present = 'true' 

if test_tgc_present == 'true':
    # now we need to find this and read it in!
    z = 1 # holding message
    os.chdir(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model")
    for file in glob.glob("*.tgc"):
        tgc_file_name = file
        print(tgc_file_name)
        # tgc_filepath = sys.path(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model\tgc_file_name") S
        tgc_file_path = os.path.join(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model", file)
        tgc_file = open(os.path.join(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Model", file))

else:
    raise Exception('.tgc file not found')

# TODO:
# Now we want to interogate the tgc file to pick out information
# Info we want: [xll, yll, dx, nrows, ncols, active_area, rotation]
# x11, yll - > lower left coordinates of box
# dx - > spacial component
# nrows, ncols- > number of rows and columns
# active_area - > as a .shp file, should be able to pull this out relatively easily
# rotation -> challenge, rotation between north south and the line we are using. 
target_variables = ['Grid Size (X,Y)', 'Cell Size']


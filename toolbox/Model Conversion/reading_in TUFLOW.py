# in this file we will be attempting to reading in a TUFLOW .tcf file and convert to a xml2d file

import sys, mmap, glob, os

sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

from floodmodeller_api import XML2D

#importing the TUFLOW data as a text file
# TUFLOW_data = open(r"C:\Users\phillio\OneDrive - Jacobs\Documents\TUFLOW_examples\Bootle\Bootle\TUFLOW\Runs\BOOT_~e1~_~s1~_~s2~_~s3~_023.tcf")
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
else:
    raise Exception('.tgc file not found')



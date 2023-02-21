# TUFLOW conversion functions. In this file we will have a list
# of functions needed for converting the TUFLOW file so it can 
# be written into an xml file and ran through Flood Modeller.

# specific packages needed:
import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona

sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

def find_ncols_nrows_gridsize(tgc_file_path):
    """ 
    In this function we are going to be reading in the tgc file and
    then partitioning the file as a string until we have the number
    of columns, rows and the grid size.

    Input args:
        path to tgc file

    Output args:
        Grid size - is the spacial step size of the grid
        ncols - is the number of columns
        nrows - is the number of rows

    Assumptions:
        1. Assuming the TUFLOW tgc file is formatted in the standard way

    
    """

    # TODO: Introduce try accept over the partitioning loop so that it will hit 
    # an error if the tgc file is not as expected.
    # opening the file as a string
    tgcfile_path = pathlib.Path(tgc_file_path)
    tgcfile = open(tgcfile_path, "r")
    tgc_file = tgcfile.read()

    # TODO: Introduce try accept over the partitioning loop so that it will hit 
    # an error if the tgc file is not as expected.

    # now partitioning the string so we can access the information
    str_partition1 = tgc_file.partition('! Cell size (metres)')
    str_partition2 = str_partition1[0].partition('! Grid dimensions (metres)')
    str_partition3 = str_partition2[0].partition('! Grid Definition')
    str_partition4 = str_partition2[2].partition('Cell Size == ')
    str_partition5 = str_partition3[2].partition('Grid Size (X,Y) == ')
    str_partition6 = str_partition5[2].partition(', ')

    Grid_size = float(str_partition4[2])
    ncols = float(str_partition6[0])
    nrows = float(str_partition6[2])

    return Grid_size, ncols, nrows



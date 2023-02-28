# TUFLOW conversion functions. In this file we will have a list
# of functions needed for converting the TUFLOW file so it can 
# be written into an xml file and ran through Flood Modeller.

# specific packages needed:
import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona
import copy

sys.path.append(r"C:\Users\phillio\Github\Open_source\floodmodeller-api")

def convert_tgc_to_list(tgc_filepath):
    '''
    In this function we will be reading in the tgc file from the specific given filepath
    and will give the output as a list of tuples, of the property and the value.

    # Input arguments:
        tgc_filepath - the path to the file
    
    # Output arguments
        tgc_data - list of tuples of the outputs
    
    # Assumptions:
        1. Tabbed spaces are interpreted as type "\t"
    '''
    with open(tgc_filepath, "r") as tgcfile:
        raw_data = [line.rstrip("\n") for line in tgcfile.readlines()]

    # cleaning the data to remove commented lines (starts with "!"" or "! ") or empty lines:
    raw_data_copy = copy.deepcopy(raw_data)
    for line in raw_data_copy:
        if line.lstrip().startswith("!"):
            raw_data.remove(line)

    raw_data_copy = copy.deepcopy(raw_data)
    for line in raw_data_copy:
        if line.lstrip().startswith("! "):
            raw_data.remove(line)

    raw_data_copy = copy.deepcopy(raw_data)
    for line in raw_data_copy:
        if len(line.strip()) == 0:
            raw_data.remove(line)

    # removing any tabbed spaces
    raw_data = [item.replace('\t', '') for item in raw_data]

    # removing comments that are written after a useful argument
    for line in range(len(raw_data)):
        line_partition = raw_data[line].partition('!')
        raw_data[line] = line_partition[0] # only taking information from the left habd side if the '!'

    # now we are splitting the data so we have the tuple, (properties, value) being appended to a list
    tgc_data = []
    for line in raw_data:
        # print(line)
        if '==' in line:
            prop, value = [itm.strip() for itm in line.split('==', 1)]

            tgc_data.append((prop, value))

    return tgc_data


def place_holder_name(tgc_data):
    ''' 
    In this function we will be isolating information for the tgc file for constructing
    the computational area for Flood Modeller

    Inputs:
        tgc_data - list of data

    Outputs
        xll
        yll
        nrows
        ncols
        active_area
        rotation

    Assumptions:
        1.
    '''
    # finding the path for the loc line
    loc_line = 1 # holding for time being
    # now need to open the file
    loc_line.open('a')
    df_loc_line = gpd.read_file(loc_line)

    #isolating xll, yll
    orientation_line = df_loc_line.gemoetry[0]
    x1, y1 = orientation_line[0]
    x2, y2 = orientation_line[1]


def find_orientation_line_angle(x1, y1, x2, y2):
    '''
    Here we will find the angle between the horizontal x axis originating 
    at (x1, y1) and the point (x2, y2) anti clockwise from x axis, the angle
    will range from 0 to 360 degrees.

    Input:
        (x1, y1) start point of the orientation line
        (x2, y2) end point of the orientation line

    Output:
        Theta - angle between the horizontal and the orientation line in anti-clockwise line

    Assumptions:
        1. angle is measured anti clockwise from horizontal, centre of rotation (x1, y1).
    '''
    if y2 > y1: # restriction to the upper half plane
    dy = y2 - y1

    if x2 > x1:  #first qudarant \theta \in (0, 90)
        dx = x2 - x1
        theta = math.degrees( math.atan(dy/dx) )
        return theta
    elif x2 == x1: # y = x line
        theta = 90
        return theta
    elif x2 < x1: #second quadrant\theta \in (90, 180)
        dx = x1 - x2
        theta_int = math.degrees( math.atan(dx/dy) )
        theta = 90 + theta_int
        return theta

    elif y2 == y1: # here we are already on the x axis, just depends on which side of the y=x line we are.

        if x2> x1:
            theta = 0
            return theta
        elif x2 < x1:
            theta = 180
            return theta

    elif y2 < y1: # restriction to the lower half plane
        dy = y1 - y2 

        if x2 < x1: # third qudrant \theta \in (180, 270)
            dx = x1 - x2
            theta_int = math.degrees( math.atan( dy/dx ) )
            theta = 180 + theta_int
            return theta

        elif x2 == x1: # y = x line again
            theta = 270
            return theta
        
        elif x2 > x1:  # fourth quadrant, \theta \in (270, 360)
            dx = x2 - x1
            theta_int = math.degrees( math.atan(dy/dx) )
            theta = 270 + theta_int
            return theta

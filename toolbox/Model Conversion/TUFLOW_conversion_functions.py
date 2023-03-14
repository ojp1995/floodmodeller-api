# TUFLOW conversion functions. In this file we will have a list
# of functions needed for converting the TUFLOW file so it can 
# be written into an xml file and ran through Flood Modeller.

# specific packages needed:
import pathlib 
import sys, mmap, glob, os
import geopandas as gpd
import pyproj, fiona
import copy
import shutil  # for copying files to new file paths
import math
import pandas as pd

def convert_tgc_to_list(tgc_filepath):
    '''
    In this function we will be reading in the tgc file from the specific given filepath
    and will give the output as a list of tuples, of the property and the value.

    # Input arguments:
        tgc_filepath - path to tgc file. Type - Path
    
    # Output arguments
        tgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
    
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

    # final step to remove properties with two values or extra unwanted string
    tgc_data = clean_space_from_tgc(tgc_data)

    return tgc_data

def clean_space_from_tgc(tgc_data):
    '''
    In this function we will be attempting to clean the data so everything is either an integer or a string.
    
    Inputs
        tgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
    
    Outputs
        tgc_data - This will be cleaned to split any entries that are partitioned are given their own value. Type - List of Tuples
    
    Assumptions:
        1. Partitionaing around | 
        2. That on at least one side of the | there is something useful we want
        3. There is only one | per line.
        '''

    # We are wanting to see if there are any spaces in the values and remove those as they should be either numbers
    # or strings.
    #
    # HOWEVER, we want to leave the 'GRID SIZE (X,Y)' as is as we deal with that separately

    for line in range(len(tgc_data)):
        if '|' in tgc_data[line][1]:  # partitioning around |, sometimes I don't think we want the info
            tgc_line_partition = tgc_data[line][1].partition('|')
            
            # check that left of | contains a .shp file
            if '.shp' in tgc_line_partition[0]:
                tgc_data[line] = (tgc_data[line][0], tgc_line_partition[0].strip())
            else:
                tgc_data.remove(tgc_data[line])

            if '.shp' in tgc_line_partition[2]:
                tgc_data.append( (tgc_data[line][0], tgc_line_partition[2].strip()) )

    return tgc_data


def find_active_area_from_tgc_file(tgc_data, tgc_filepath, FM_folder_path):
    ''' 
    In this function we will be isolating information for the tgc file for constructing
    the computational area for Flood Modeller

    Inputs:
        ttgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
        tgc_filepath - path to tgc data. Type - Path
        FM_folder_path - path to Flood Modeller folder where we want the data saved to. Type - Path
        

    Outputs 
        xll - lower left x-coordinate of the computational area. Type - Float
        yll - lower left y-coordinate of the computational area. Type - Float
        dx - spacial step - Type - Float
        nrows - number of rows in the computational area, Y direction n_Y/dx. Type - Integer
        ncols - number of colums in the computational area, X direction n_X/dx. Type - Integer
        active_area - path to active area file in FM folder. Type - Path
        rotation - angle rotational area is rotated in anti-clockwise direction from the horizontal
            between 0 and 360 degrees. Type - Float

    Assumptions:
        1. rotation is output in degrees. Angle is measured from horizontal anti-clockwise
    '''
        # now we need to find the nrows, ncols, and active area path
    for line in range(len(tgc_data)):
        if tgc_data[line][0] == 'Cell Size':
            dx = float(tgc_data[line][1])
        
        if tgc_data[line][0] == 'Grid Size (X,Y)':
            line_partition = tgc_data[line][1].partition(',')
            n_X = float(line_partition[0])
            n_Y = float(line_partition[2])
        
        if tgc_data[line][0] == 'Read GIS Code':
            active_area_rel_path = tgc_data[line][1]

        if tgc_data[line][0] == 'Read GIS Location':
            orientation_line_path = tgc_data[line][1]


    # finding the parent path of the tgc file 
    p = pathlib.Path(tgc_filepath)
    parent_path = p.parents[0]

    # active area path
    active_area_path_TF = pathlib.Path.joinpath(parent_path, active_area_rel_path)
    active_area_file_name = active_area_path_TF.name

    # read the file using geopandas
    df_active_area = gpd.read_file(active_area_path_TF)
    # move the file to the new location
    df_active_area.to_file(pathlib.Path(FM_folder_path, active_area_path_TF.name))

    active_area_path_FM = pathlib.Path.joinpath(FM_folder_path, active_area_file_name)

    # orientation line path construction and using the orientation line to access info for active area
    orientation_line_file = pathlib.Path.joinpath(parent_path, orientation_line_path)  # holding line for the minute
    
    orientation_line_file.open('a')
    df_orientation_line = gpd.read_file(orientation_line_file)

    
    #isolating xll, yll
    orientation_line = df_orientation_line.geometry[0]
    x1, y1 = orientation_line.coords[0]
    x2, y2 = orientation_line.coords[1]
    
    xll, yll = x1, y1

    # computing the rotation
    rotation = find_orientation_line_angle(x1, y1, x2, y2)


    ncols = int(n_X/dx)
    nrows = int(n_Y/dx) 
    
    return xll, yll, dx, nrows, ncols, active_area_path_FM, rotation


def find_orientation_line_angle(x1, y1, x2, y2):
    '''
    Here we will find the angle between the horizontal x axis originating 
    at (x1, y1) and the point (x2, y2) anti clockwise from x axis, the angle
    will range from 0 to 360 degrees.

    Input:
        (x1, y1) start point of the orientation line. Type Float
        (x2, y2) end point of the orientation line. Type Float

    Output:
        Theta - angle between the horizontal and the orientation line in anti-clockwise line. Type Float

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

    
def load_active_area_to_xml(xml2d, xll, yll, dx, nrows, ncols, active_area_path, rotation, FM_folder_name, domain_name):
    '''
    Here we will be adding the information needed for the computational area for 
    Flood Modeller xml2d solver

    Inputs:
        xll - lower left x-coordinate of the computational area. Type - Float
        yll - lower left y-coordinate of the computational area. Type - Float
        dx - spacial step - Type - Float
        nrows - number of rows in the computational area. Type - Integer
        ncols - number of colums in the computational area. Type - Integer
        active_area - path to active area file in FM folder. Type - Path
        rotation - angle rotational area is rotated in anti-clockwise direction from the horizontal
                    between 0 and 360 degrees. Type - Float
        domain_name - the domain we are wanting to add here. Type String

    Outputs:
        xml2d - updated with computational area. Type xml file

    Assumptions:
        1. Empty (ish) xml2d file as input, or rather no computational area 

        2. Angle is measured from the lower left coordinate from the horizontal in the anti-cloclwise direction

        3. xml2d is at the same level as the folder, FM_folder.

        4. active_area_path is an absolute path.
    '''

    active_area_file = pathlib.Path(active_area_path).name
    active_area_path_FM = pathlib.Path(FM_folder_name, active_area_file)

    xml2d.domains[domain_name]["computational_area"]["xll"] = xll
    xml2d.domains[domain_name]["computational_area"]["yll"] = yll
    xml2d.domains[domain_name]["computational_area"]["dx"] = dx
    xml2d.domains[domain_name]["computational_area"]["nrows"] = nrows
    xml2d.domains[domain_name]["computational_area"]["ncols"] = ncols
    xml2d.domains[domain_name]["computational_area"]["active_area"] = str(active_area_path_FM)
    xml2d.domains[domain_name]["computational_area"]["rotation"] = rotation

    return xml2d

def find_and_load_asc_to_xml(xml2d, tgc_data, tgc_folder_path, FM_folder_path, domain_name):
    '''
    In this function we will be finding the asc file and copying it to the new folder. Looking for property 
    "Read Grid Zpts"

    Input
        xml2d - xml2d file without/with old asc file path. Type xml file
        tgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
        tgc_filepath - path to tgc file. Type - Path
        FM_folder_path - path to Flood Modeller folder where we want the data saved to. Type - Path
        domain_name - the domain we are wanting to add here. Type String

    Output
        xml2d - with path to new asc file. Type xml file.

    Assumptions
    '''
    for line in range(len(tgc_data)):
        if tgc_data[line][0] == 'Read Grid Zpts':
            asc_file= tgc_data[line][1]

    asc_file_path_TF = pathlib.Path(tgc_folder_path, asc_file) # isolating TUFLOW path
    shutil.copy(asc_file_path_TF, FM_folder_path)  # copying the file across
    asc_file_path_FM = pathlib.Path(FM_folder_path.parts[-1], pathlib.Path(asc_file).name)  # file path for FM repo

    xml2d.domains[domain_name]["topography"] = str(asc_file_path_FM)  # adding asc to xml file

    return xml2d

def find_and_copy_roughness_to_FM_repo(xml2d, tgc_data, tgc_folder_path, FM_folder_path, df_tmf):
    '''
    In this function we will be looking at the data and then finding the roughness with the 
    property 'Read GIS Mat'. It will also load the associated roughness values to a new column
    of the shape files before being exported.

    Inputs
        tgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
        tgc_filepath - path to tgc file. Type - Path
        FM_folder_path - path to Flood Modeller folder where we want the data saved to. Type - Path
        df_tmf - data frame with the roughness values with associated material code IDs

    Outputs:
        df_complete - This is the data frame of the roughness

    Assumption: 
        1. Data is clean
        2. The material code/ ID matches between the df_tmf and the roughness ID values given.
    '''
    roughness = []
    for line in range(len(tgc_data)):  # looping through to find all relevant roughness shp files
        if tgc_data[line][0] == 'Read GIS Mat':
            roughness.append(tgc_data[line][1])

    # now we want to open and then copy the shape file(s) across
    for j in range(len(roughness)):
        # path to file
        roughness_path_TF = pathlib.Path(tgc_folder_path, roughness[j])
        # open the file
        df_roughness = gpd.read_file(roughness_path_TF)
        # attaching the roughness manning values to specific material code IDs
        # finding which column contains the associated material codes
        S1 = set(df_tmf['Type/ID'])  # set of ID's we are using as the reference        
        for col in df_roughness.columns:
            S2 = set(df_roughness[col])  # set of each columns values

            if len(S1.intersection(S2)) != 0:  # checking to see that the intersection of sets is not empty
                # merging the two data frames so they have the corresponding values
                df_complete = df_roughness.merge(df_tmf, how='inner', left_on = col, right_on = 'Type/ID')

        # move file to FM folder
        df_complete.to_file(pathlib.Path(FM_folder_path, roughness_path_TF.name))

    return xml2d

def find_mannings_val_from_tmf(tmf_file):
    '''
    We will be reading the tmf file, cleaning it and exporting it as a data frame. There will be (hopefully)
    two columns, one with the material code, one with the associated mannings value for roughness.

    Inputs
        tmf_file -  File with material codes and corresponding roughness.

    Outputs
        df_tmf - data frame with the roughness values with associated material code IDs.


    Assumptions:
    '''

    with open(tmf_file, "r") as tmffile:
        raw_data = [line.rstrip("\n") for line in tmffile.readlines()]

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

    # removing comments on RHS of useful data
    for line in range(len(raw_data)):
        line_partition = raw_data[line].partition('!')
        raw_data[line] = line_partition[0] # only taking information from the left habd side if the '!'

    # now splitting around the comma so we have ID code and corresponding value
    tmf_data = []
    for line in raw_data:
        if ',' in line:
            data_partition = line.partition(',')
            material_code = data_partition[0].strip()
            value = data_partition[2].strip()

            tmf_data.append((int(material_code), float(value)))

    # now we want to export this as a data frame for easy handling
    df_tmf = pd.DataFrame(tmf_data, columns = ['Type/ID', 'value'])

    return df_tmf
    
def load_roughness_to_xml(xml2d, tgc_data, FM_folder_path, domain_name):
    '''
    In this function we will be loading the roughness parameters to the xml. 

    Inputs
        xml2d - xml2d file without/with old asc file path. Type xml file
        tgc_data - List of tuples from tgc file, tuples as (properties, values). Type - List of Tuples
        FM_folder_path - path to Flood Modeller folder where we want the data saved to. Type - Path
        domain_name - the domain we are wanting to add here. Type String
        

    Outputs:
        xml2d - the updated xml with paths to roughness files.

    Assumptions:
        1. A blank domain is inserted with only one entry, multiple entries would need a different routine
        2. Currently only type is set to file and law to manning, need to find a way to adapt that.

    '''

    #TODO: Add ability to know whether this is going to be a a different type or law.
    roughness_value = []
    # finding the roughness values we need to add.
    for line in range(len(tgc_data)):
        if tgc_data[line][0] == 'Read GIS Mat':
            roughness_value.append( str(pathlib.Path(FM_folder_path.parts[-1], pathlib.Path(tgc_data[line][1]).name)) )

    xml2d.domains[domain_name]["roughness"] = []  # creating blank

    for j in range(len(roughness_value)):
        xml2d.domains[domain_name]["roughness"].append(
            {"type": "file", "law": "manning", "value": roughness_value[j]}
        )




    return xml2d
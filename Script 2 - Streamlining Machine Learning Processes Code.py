# -*- coding: utf-8 -*-
####################################################################################################################################
#
# Author: Emily Evenden
# Final Project: Streamling Machine Learning Processes using Python and the TerrSet IDRISI API
# Due: Oct. 6th, 2019
# Time: ~20 hours
#
####################################################################################################################################
#
# This script was made as my final project for Python Programming at Clark University.
#
# Context:  At Clark Labs, machine learning tools are frequently used to classify
# difficult land-cover types such as mangrove forests. However, to use these tools,
# there is a significant amount of data preparation and clean up done manually.
#
# For my final project, I developed a script which streamlines part of the
# classification procedure used in Clark Labs. This script takes in
# user-made training sites for mangrove forest classification, creates several files used in
# in the IDRISI tools; automatically creates a signature file; runs the machine
# learning module; and returns a binary & filtered raster of potential mangrove forest locations.
#
# This is done using the IDRISI API which can both interact with Python and houses a python
# library of IDRISI Geoprocessing tools. I chose this as my final project because, currently,
# we don’t have an automated way to update the machine learning outcomes when we add or remove training sites.
#
# If you would like to run this file, you will need to a Terrset license and you will need to install PyWin32
# found at this link: https://sourceforge.net/projects/pywin32/files/pywin32/
#
# In addition, I have provided some sample data in my GitHub repo which can be used with this script.
# Download the data and change the IDRISI and os working directories in this script to the file on your computer.
#
###################################################################################################################################



### Part 1: Creating Training Sites
#
# User creates a vector file of mangrove training sites in Terrset using the digitize tool. All training sites
# should use the same integer value to indIcate they all represent one land-cover type, i.e. all mangrove sites
# should have a value of 1.
#
# This is saved as a vector file.
# An example file is provided in the downloadable sample data file.



###################################################################################################################################



### Part 2: Directory Set Up
#
# This sets up the directories used in the code



# Imports Windows Python client
import win32com.client

# Import operating system interface. This allows Python to interact with the Windows operating system.
import os

# Set IDRISI API to variable IDRISI32 so the rest of the script can access Terrset IDRISI API
IDRISI32 = win32com.client.Dispatch('IDRISI32.IdrisiAPIServer')

# Print statement to make sure set up is finished
print "Settings Prepared"

# Set IDRISI working directory path the data folder. If you are using this code, you must update the file path here. 
IDRISI32.SetWorkingDir("C:\Users\EEvenden\Documents\Python\Final Project\Data\Prep_1")

# Set the script's working directory to same data folder. This script creates several files outside
# of the IDRISI library, and therefore needs a directory as well.
os.chdir("C:\Users\EEvenden\Documents\Python\Final Project\Data\Prep_1")

# Print statement to ensure working directory is set
print "Working Directory Set"



####################################################################################################################################



### Part 3: Metadata File Creation
#
# Here, several files are created which will be used as inputs for the IDRISI tools later on.



### Metadata File 1: Create text file to assign a category name to the spectral signature created via MAKESIG.
# This is one of the inputs for the function.

# First, we must create a text file and write text to it
category = open("Mangrove_Category.txt", "w+")

# This is the format of labeling used in MAKESIG
category.write("1 mangrove")

#Save & close the text file
category.close()
print "Category assigned"



### Metadata File 2: Create a second file with the category name as group signature file' This is an input
# for the MAHAlCLASS machine learning function. I am not sure why this isn't programmed as a MakeSig function
# outputs, but this file needs to exist to run MAHALCLASS. It helps the toold for the .sig and .SPF files
# created by MAKESIG.

# Repeat the same steps as above
# First, we must create a text file and write text to it
category = open("mangrove_training.txt", "w+")

# This is the format of labeling used in MAKESIG
category.write("""1
               Mangrove""")

#Save & close the text file
category.close()


# Terrset will not accept a signature group file with the .txt extension
# Here, we parse our file name and add a Terrset-specific file extension (.sgf)
change_Ex = "mangrove_training.txt"
base = os.path.splitext(change_Ex)[0]
os.rename(change_Ex, base + ".sgf")

print "Category assigned"



### Metadata File 3: Create a raster group file of all the rasters used to make the spectral signatures in MAKESIG
# To do this, first make a text file again and write in it
mangrove_rgf = open("Mangrove_Class.txt", "w+")

# This is the format used to create a raster group file in Terrset.
# From what I could find, there is not function in the IDRISI library that automatically makes RGFs. So I had to
# find a way to do it outside of IDRISI
mangrove_rgf.write ("""3
Tass_LT05_L1TP_151044_19990424_20180710_01_T1_moist
Tass_LT05_L1TP_151044_19990424_20180710_01_T1_green
DEM_LT05_L1TP_151044_19990424_20180710_01_T1""")

# Save & close the text file
mangrove_rgf.close()

# In addition, Terrset will not accept a raster group file with the .txt extension
# Here, we parse our file name and add a Terrset-specific file extension (.rgf)
change_Ex = "Mangrove_Class.txt"
base = os.path.splitext(change_Ex)[0]
os.rename(change_Ex, base + ".rgf")

# Print statement to show .rgf file is created
print "RGF file created"



### Metadata File 4: Create another text file assigning a threshold for the RECLASS function. The threshold
# will filter out low probability pixels identified by the machine learning funtion as mangrove.
#
# To set the threshold, a text file must be created and input to the RECLASS function
# Here, a new text file is created
myfile = open("Mangrove_Threshold.txt", 'w+')
print "File Open"

# The text is entered into the file. A vlaue of 1 is set to pixels with a suitability of .01 or higher
myfile.write("1 .01 >")

#Close file
myfile.close()
print "Thresholds set"

# Again, Terrset will not accept attribute file with the .txt extension
# Here, we parse our file name again and add a Terrset-specific file extension (.rcl)
change_Ex = "Mangrove_Threshold.txt"
base = os.path.splitext(change_Ex)[0]
os.rename(change_Ex, base + ".rcl")



#####################################################################################################################



### Part 4: Create a Spectral Signature File 

### Run the MakeSig function to make the spectral signature file used for MahalClass machine learning hard classifier.
#
# --- Explanation for arguements used in the function ---
#
# v = vector (input used to create signature sites)
# 30 = minimum number of pixels needed to create the signatures. This is equal to 10 pixels per raster in the raster
#   group fileused later.
# Mangrove_Class.rgf = the raster group file created in Part 2 containing rasters with information for each training
#   site. In this case, the raster group file
#   contains three files containing information about elevation, water-soil saturation, and plant "greeness" (similar
#   to NDVI).
#   At Clark Labs, these files are automatically created and available when we run the initial file import module made ofr this project.
# Mangrove_Category.txt = the file created in Part 2 containing the associated integer and name of the category
#   (i.e. Mangrove). Text file is pulled in and sets the category name within the function.
IDRISI32.RunModule('MAKESIG','v*mangrove_training.vct*30*Mangrove_Class.rgf*Mangrove_Category.txt', 1, "", "", "", "", 1)
print "MakeSig completed"



###########################################################################################################################



### Part 5: Running the Mahalanobis function to classify Mangrove forest patches

### Run the MAHALCLASS function to classify all Mangrove forestd
#
# --- Explanation for arguement used in the function ---
# mangrove_training.sgf = spectral signature file created in Part 2. These file name is identical the name of the
#   vector file used to create
#   the training sites in part 2.
IDRISI32.RunModule('MAHALCLASS', 'mangrove_training.sgf*mahal', 1, '','','','', 1)
print "Mahal completed"

# Mask the Mahal output by our study area. This gets rid of any selected pixels outside the area of interest
IDRISI32.RunModule('OVERLAY', '3*Mask_StudyArea_LT05_L1TP_151044_19990424_20180710_01_T1.rst*mahalMangrove.rst*masked_mangrove', 1, '', '', '', '', 1)
print "Mask completed"



###################################################################################################################################


                           
### Part 6: Reclass MAHALCLASS output to filter pixel which fall under pred-determined suitability threshold

### Create text file containing Mangrove forest threshold.
#
# --- Explanation of threshold ---
#
# Part 3 (MAHALCLASS) out puts a map of suitability for mangrove forests. Areas with a higher suitability value are more likely to be mangrove forests.
# In order to make a map of mangrove forests with reduced noise from classification errors, a threshold is used to filter out suggested mangrove forests
#   pixels with a lower suitability value. In this case, the threshol dis set to a suitability of .01. Any pixel with a value less than .01 will be
#   removed from the results
#
### Run the RECLASS function to filter the MAHALCLASS output using the thresholds created
#
# --- Explanation of RECLASS Arguments ---
# i = file type being reclasses (i= raster image)
# maked_mangrove.rst = the MAHALCLASS output is set as the reclass input
# Mangrove_Reclass.rst = output name
# Mangrove_Threshold.rcl = the threshold text file created in Part 2
# 1 = data type for output (1 = byte/integer)

IDRISI32.RunModule('RECLASS' ,'i*masked_mangrove.rst*Mangrove_Reclass.rst*3*Mangrove_Threshold.rcl*1', 1, "", "", "", "", 1)

#Print statement to ensure Reclass is completed
print "Reclass completed"



###################################################################################################################################



### Part 7: Breakout Reclassified Mangrove

### Create a  new file of only pixels reclassified to 1. All other pixels will be considered background pixels
#
# --- Explanation for BREAKOUT arguments ---
# 1 = file type (1 = raster image)
# Mangrove_Reclass.rst = input for BREAKOUT (the output from RECLASS)
# Mangrove_Breakout.rst = name of output
# 2 = Breakout option (2 = breakout one class, not all classes)
# 1 = class identifier (1 = mangrove class in the Reclass file)
IDRISI32.RunModule('BREAKOUT', '1*Mangrove_Reclass.rst*Mangrove_Breakout.rst*2*1', 1, "", "", "", "", 1)

#Print statement to ensure Breakout works
print "Breakout completed"



############################################################################################################################



### Part 8: Clean up Final Output using FILTER.

### Filter the breakout file to remove pixel noise. This tool specifically uses a user-specified matrix to smooth
# the pixel values. This tool is actually not used in the Clark Labs procedure but the AREAFILTER function is used
# is not publically available on version 18 of Terrset.
#
# --- Explanation of FILTER arguments ---
# Mangrove_Breakout.rst = the BREAKOUT output is used to filter out pixel noise
# Mangrove_Final = output name
# 3 = Filter type. In this case, "3" means I will filter my image by mode. i.e. pixels will be comverted to the mode of the
#   surrounding pixels. I selected this because the breakout out put is binary, only showing pixels with a value of
#   1 or 0. S0 - if we want convert noise pixels to whole values of 0 or 1 (rather than decimals), the mode should be
#   able to do this in a simple way.
# 3 = the size of the filter matrix. In this case, pixels will be compared within a 3x3 pixel matrix.
IDRISI32.RunModule('FILTER', 'Mangrove_Breakout.rst*Mangrove_Final*3*3', 1, '', '', '', '', 1)

#Print statement to ensure Filter worked
print "Final Mangrove Classification Complete"



#####################################################################################################################################



# Final Output Comments

# To view the results of this script. Overlay the Mangrove_Final.rst onto the Comp354 image. (Make the bakcground values of
# Mangrove_Final transparent. You will see that the main, dark red/organe features have been highlighted. These are mangrove
# patches. 



#####################################################################################################################################



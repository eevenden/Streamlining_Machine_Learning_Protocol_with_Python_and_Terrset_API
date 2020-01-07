# Final Project
Author: Emily Evenden

Date: October 5, 2019

## Part 1: Web-Scraping Weather Data
  
  The purpose of Script 1 is to scrape a five-day weather forecast from the provided url and print the selected information in a legible format. 
  
  More specfically, the script uses the "requests" and "BeauifulSoup" libraries to call pre-made web-scraping functions. Then, the user is prompted for the latitude and longitude of the location where they would like to know the five-day forecast. These coordinates are converted to string features and input to a provided url. This searches for the five-day forecast in the location automatically. 
  
  To scrape this data, the requests.get() function is used to copy the back-end content of the webpage. Then, a html-parser within BeautifulSoup is used to split the content using HTML tags. Next, the BeautifulSoup findall() function is used to find all html classes named "forecast-tombstone". This selects the information in the daily forecast sections of the website.
  
  Finally, the stylization was done by looping through each "forecast-tombstone" class using the .replace() function to format the string outputs.
  
  I was successful in making this script run in the online complier provided in class. Though, I haven't tried it in an off-line complier. I could definitely see myself using web-scraping in the future to collect data. In the past, I've learned about web-scraping but never had the opportunity to look at any code or extract data. From what I can tell, it seems like it would be really tedious to format the information after extracting it. Also, I assume there are other library tools to convert it to an excel table. I am definitely excited to try it some more!
  
  
## Part 2: Streamlining Machine Learning Processes using Python and the TerrSet IDRISI API

  I developed the second script to correspond with the research project I work under at Clark Labs. For some context, the project uses machine learning tools within the TerrSet program to classify tricky land-cover types in Southeast Asia. One of these is Mangrove forests, which is the example I used in my script.
  
  The purpose of this script is to automate part of the classification procedure used to identify mangrove forests. The procedure itself requires using several TerrSet tools first to create training sites manually, then utilze this vector file to create spectral signatures of mangrove forest. The spectral signature are then pluggged into the machine learning function, and finally the raster output is cleaned up and filtered to remove pixel noise. Right now, we don't have an automated way to do this and instead keep multiple toolbox windows open and update them manually in succession if, for example, we want change the number of training sites used or alter the parameters which seleect mangrove forest pixels, etc. 
  
  My script has eight distinct parts, each of which has a different purpose in the procedure and uses different tools to accomplish a tasks. They are divided as follows. (Complete details about their inputs are provided in the code comments).
  
  ### Part 1: Creating Training Sites
  There isn't any code for Part 1, but it's a place holder for the main input required for the script which is a vector file of training sites. This is created manually by the user. Based on a composite image, the user would select a few obvious mangrove areas and digitze them. This vector file is then an input for Part 4. 
  
  ### Part 2: Directory Set Up
  The second part sets of the necessary libraries and directory paths for the script. This code utilizes the IDRISI Geoprocessing tool library which can be accessed with a TerrSet license. It also uses "os" to set directory connections to the computer running the code. In order to make this script run and access the TerrSet API, one must download PyWin32 for Python 2.7. A link is provided in the comments of the code.
  
  ### Part 3: Metadata File Creation
  This is probably the most confusing part of the code because it automatically creates several files needed as inputs for the IDRISI tools. They are a bit out of context and could probably be organized better (i.e. matched to the specific section they are used in). But it was easier to write them all together. 
  
  The following list of metadata files are created in the script. For the most part, they are text files with TerrSet-specfic extensions. I decided to make the files manually as an extra challenge. (Otherwise, I would need to run the procedure manually in Terrset to get these specific outputs, and then call them in my code which felt like a cheap way to make the code work). This way, I figure out how to make custom files with TerrSet extensions without messing around in the actual program.
  
  1. Mangrove_Category.txt - an input for the MAKESIG function in Part 4. This file stores the category name of the land-use type we're classigying, i.e. Mangrove
  
  2. mangrove_training.sgf - an input for the MAHALCLASS function in Part 5. It associates two output files from MAKESIG togther so that they are called together as inputs to MAHALCLASS. It's nearly identical to Mangrove_Category.txt but with a different file extension.
  
  3. Mangrove_Class.rgf - another  input for MAKESIG in Part 4. This creates raster group file (.rgf) of three images used to classify mangrove forests. Specifically, these images contain elevation, water saturation, and 'green-ness' information.
  
  4. Mangrove_Threshold.rcl - an input for RECLASS in Part 6. This text file contains the threshold by which to classify mangrove based on a suitability map.
  
  ### Part 4: Create a Spectral Signature File
  This is the first section which uses the IDRISI library. In it, I use the MAKESIG function to create a spectral signature file for the mangrove land-use type. Essentially, the manually-created vector file with the training sites is used to sample the raster group file created in Part 3. This stores the values of elevation, water saturation, and green-ness unique to mangroves and outputs two files, .sig and .SPF which store that info. The mangrove_training.sgf created in Part 3 associates the .sig and .SPF together so they can be called as a single unit later in the code. 
  
  ### Part 5: Running the Mahalanobis Machine Learning function to classify all Mangrove forests
  Next, the MAHALCLASS function is used to classify mangrove forests. It uses mangrove_training.sgf as an input and outputs a suitability map. Each pixel in the suitability map is assigned a likelihood that they are mangrove forest. 
  
  In this section, I also use the OVERLAY tool to mask out pixels outside of the sample study area. 
  
  ### Part 6: Reclass Mahalanobis output using a pre-determined suitability threshold
  In Part 6, the RECLASS tool is used to create hard classes of Mangrove and Not-Mangrove using a threshold. The .rcl file created in Part 3 contains our threshold. Specifically, we classify anything with a liklihood below .01 as not mangrove, and anything equal to or above .01 as mangrove. The output of this tools is a raster with two categories, 0 and 1. 
  
  ### Part 7: Breakout Reclassified Mangrove
   Part 7 uses the BREAKOUT tool to create a file where Mangroves are the only pixels with values other than zero. Essentially, it takes the RECLASS output and extracts all pixels with the value of 1 (i.e. Mangrove) and assigns all other pixels as the background of the image.
  
  ### Part 8: Clean up Final Output using FILTER.
   As the final step, the FILTER function is used to remove pixel noise from the final raster image. This is not actually in the procedure used by Clark Labs, but the AREAFILTER tool we normally use is not availble in version 18 of TerrSet. Therefore, I limited by what tools were available. Using FILTER, I specifically chose smooth the image using a 3x3 pixel matrix and assign odd pixels to the mode (most frequent value) of the 3x3 grid. I chose to this because there cannot be partial classifications (i.e. decimals) in the final output. So by assigning values to the mode, it has to be either 1 (Mangrove) or 0 (Not Mangrove).
   


To view the final mangrove selection, one should overlay the Final Output onto a composite. This will show what areas of the scene have been identified as mangrove. 

   
 ### Comments on the Script Development
  In some ways, designing this script was both easy and difficult. It was easy because I already had the procedure and most of the tools laid out and selected for me. As far as organizng the script, I just divided each section by which tool we use.
  
  However, because TerrSet is not widley used outside of academia, there isn't a lot of doumentation on how to use the Python API nor forums on how to troubleshoot problems. To figure out how to input the parameters properly for the geoprocessing tools, I had to ask the software's main programmer to inspect the syntax. However, once I figured the syntax out, it was fairly straight-forward.
  
  Another problem I ran into was that not all the tools in TerrSet are programmed into the python library and certain things, like making those metadata files in Part 3, have to be created directly. I think both of these issues are the result of the software being fairly small and in development. This partially limited what I could do as my project because other parts of our procedure use tools that either aren't available in public licenses of TerrSet or aren't in the most recent version.
  
  
### Potential Improvements
  Luckily, my code is functional and creates the outputs that I need. However, there are definitely many potential improvements.
    
    
  First, Part 7, the BREAKOUT section, is pretty much unneccesary. I kept it because I included it in my original code outline, but I could probably delete it and shift around some input/outputs and the code would be functionally the same.
  
  
  Secondly, as I mentioned before, it would be better organized if I shifted the metadatafiles into the sections they correspond to.
  
  
  Thirdly, many of the file names and paths are hard-coded into the program which is unideal. One way to improve this could be to prompt the user for the necessary file & directory name inputs and set them as variables. Instead of using the file names directly in the functions, I could call the variables instead. This would make the script more efficient for classifying multiple satelitte scenes or using same procedure for a different project. 
  
  
  Fourthly, I think this whole code could be turned into one function and perhaps run by inputting the first vector training site file, or something similar. However, I didn't have time to further develop it that way.
  
  
  In general, I think the next step to improving my coding in Python is to work with someone who is more fluent than me and have them critique my code and show me tricks on to make it more efficient. This specific code is functional, but not necessarily elegant. But hey, it works! Which I am pretty happy to have pulled-off.
  
  

'''

# Assignment title: Final Project- Web-scraping Weather Forecast\

# By: Emily Evenden

# Date: 10/04/2019

# Description: The script web-scrapes the weather.gov website to extract the 5-Day weather forecast for a given location. Then it stylizes the output.

# Inputs: Latitude & Longitude in Decimal Degrees
# Outputs: 5-Day Weather Forecast stylized & in all-caps

'''
# import required libraries
import requests
from bs4 import BeautifulSoup

# List to store response
forecast = []

#For the latitude and longtitude, I used the "prompt" function to ask the user for an input. I used the "str" function to convert the inputs to strings. Then, the inputs are assigned to corresponding variable names

lat = str(input("What is your latitude in decimal degrees? "))
lon = str(input("What is your longitude in decimal degrees? "))

# Here, ae url for the requested location is concatenated using the variables above
url = 'https://forecast.weather.gov/MapClick.php?lat='+lat+"&lon="+lon
print "\nChecking: " + url

# The get() function from  the "requests" library is used to retrieve the information from the url
# The page variable stores the text from the webpage

page = requests.get(url)

# A BeautifulSoup object stores the text from the URL
# One can access the contents of the web-page using ".content"
# Then "html_parser" is used since our page is in HTML format

soup=BeautifulSoup(page.content,"html.parser")

# The "findAll()" function locates all occurrences of div tag with the given class name
# and stores it in the BeautifulSoup object

weather_forecast = soup.findAll("li", {"class": "forecast-tombstone"})

# This for loop cycles through the BeautifulSoup object to extract text from every class instance using .text and stores the results in a list

for i in weather_forecast:
  i = i.text
  forecast.append(i)

# Print list to remove unicode characters and format the output
for day in forecast:
  #Adds spaces behind "High"
  day = day.replace("High", "; High")

  #Adds semicolon and space behind Low
  day = day.replace("Low", "; Low")

  #Adds a space in specific text
  day = day.replace("BecomingSunny", "Becoming Sunny")
  day = day.replace("ThisAfternoon", "This Afternoon")
  day = day.replace("SlightChance", "Slight Chance")
  day = day.replace("thenAreas", "then Areas")
  day = day.replace("thenMostly", "then Mostly")

  #Adds a comma and a space
  day = day.replace("then", ", then")

  #Adds spaces between words
  day = day.replace("Likely", " Likely")
  day = day.replace("yNight", "y Night")

  #Adds space after "Chance" and the word "of"
  day = day.replace("ChanceShowers", "Chance of Showers")
   
  #Removes a space after "Clear"
  day = day.replace("Clear ", "Clear")

  #Adds a space before Mostly
  day = day.replace("Mostly", " Mostly")

  #Removes a space in a specific instance of "Mostly"
  day = day.replace(" Mostly Clear", "Mostly Clear")
  day = day.replace(" Mostly Sunny", "Mostly Sunny")
   
    #Removes a space between "Showers" and "," and adds "of"
  day = day.replace("Showers ,", "Showers,")
  
  #Finally, we convert the entire text to uppercase
  day = day.upper()
  print day

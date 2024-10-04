## Purpose
  The goal of this project is to write a console-based Python program that inputs
  commands from the user and outputs data from the CTA2 L daily ridership database.
  SQL should be used to retrieve and compute most of the information, while Python is
  used to display the results and if the user chooses, to plot as well.

## Commands
  There are 9 commands. 

  1. Find Stations by Name (uses user input for the station name)
  Description: Lists all station names and IDs that match the user's input.

  2. Analyze Station Ridership (uses user input for the station name)
  Description: Shows the percentage of riders on weekdays, Saturdays, and Sundays/holidays for a specific station.
  
  3. Weekday Ridership for All Stations 
  Description: Outputs total ridership on weekdays for each station, along with their percentages of the total ridership.
  
  4. Stops for a Line and Direction (uses user input for the line color and direction)
  Description: Lists all stops for a given line color and direction, indicating ADA accessibility.

  5. Number of Stops by Color and Direction 
  Description: Shows the number of stops for each line color, separated by direction, along with their percentages of the total number of    stops.

  6. Yearly Ridership for a Station (uses user input for station name + year) 
  Description: Outputs total ridership for each year for a specified station. You can also plot this information.


  7. Monthly Ridership for a Station and Year (uses user input for station name and year)
  Description: Provides total ridership for each month in a specified year for a given station. You can also plot this information.

  8. Compare Daily Ridership Between Two Stations (uses user input for 2 stations and a year)
  Description: Outputs daily ridership totals for two specified stations in a given year. You can also plot this information into a
  comparable plot.

  9. Find Stations Near a Location 
  Description: Lists all stations within a mile of specified latitude and longitude coordinates.
  You can also plot this information on the map of Chicago.
 

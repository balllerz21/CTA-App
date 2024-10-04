#
# Name: Maria Guallpa
# CS 341 Fall 2024
# Project 1: CTA Database App
# Summary: write a console-based Python program that inputs
# commands from the user and outputs data from the CTA2 L daily ridership database using SQL. 

#imports
import sqlite3
import matplotlib.pyplot as plt

#helper functions
#######################################################################################################

# manyStationCount:

# Given a list of results from an sql query, retrieves the count variable of the query and returns the count variable as an integer.
# This is used to check if the result list has too many stations to work with for commands 6, 7, and 8.

def manyStationsCount(result):
    tempList = [row[0] for row in result]
    count = int(tempList[0])
    return count

#######################################################################################################

# manyStationsInput:

# Given a database connection and a station name, retrieves the count of Station_IDs and Station Names that closely match the station name given.
# This function returns the list of said Station_IDs and Station Names. This function gives out the list that is used to check
# if there are too many stations to work with for command 6, 7, and 8.

def manyStationsInput(dbConn, station):
    dbCursor = dbConn.cursor()

    sqlMany = """Select count(Station_ID), Station_Name from Stations where Station_Name like ?"""
    dbCursor.execute(sqlMany, [station])

    resultMany = dbCursor.fetchall()
    return resultMany

#######################################################################################################

# manyStationCheck:

# Given a list of an sql query, checks if the list length is too long and if the list is empty. If list is empty,
# then the "No stations found" message is printed and returns False. If the list count is too long, the "too many stations"
# message is printed and returns False. Otherwise, it returns True. 

def manyStationCheck(resultMany):
    count = manyStationsCount(resultMany)

    #checks if list is empty
    if not resultMany:
        print("**No station found...")
        print()
        return False  
    _, station = resultMany[0]
    if not station:
        print("**No station found...")
        print()
        return False  
    
    #checks if list is too long
    if count > 1:
        print("**Multiple stations found...")
        print()
        return False  
    return True

#######################################################################################################

# print_stats
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.

def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General Statistics:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Stops")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    dbCursor.execute("Select count(*) From Ridership")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute("Select min(date(Ride_Date)), max(date(Ride_Date)) from Ridership")
    row = dbCursor.fetchone();
    print("  date range:", row[0], "-", row[1])

    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    print("  Total ridership:", f"{row[0]:,}")
    print()

#######################################################################################################

# Command 1:
# Given a database connection, the function prints out all the station names and station_IDs 
# that match the user input.

def command1(dbConn):
    dbCursor = dbConn.cursor()
    print()

    user_input = input("Enter partial station name (wildcards _ and %): ")
    sql = """SELECT Station_ID, Station_Name from Stations where Station_Name like ? order by Station_Name asc;"""
    dbCursor.execute(sql, [user_input])
    result = dbCursor.fetchall()

    # if no station exists, command ends
    if not result:
        print("**No stations found...")

    #prints the results
    for row in result:
        print(row[0], ":", row[1])
    print()

#######################################################################################################

# printAndMathForCommand2:
# This function prints out the results for command 2 as well as does the math to get the percentages and prints the 
# percentages as well. 

def printAndMathForCommand2(result, result2, user_input):  
    tempList = [row[0] for row in result]
    tempList2 = []
    for row in result2:
        tempList2.append(row[0]) 
    saturday, sunHoliday, weekday = tempList
    total = int(tempList2[0])

    #does math to get percentages
    percentSaturday = saturday / total * 100
    percentSunHoli = sunHoliday / total * 100
    percentWeekday = (weekday / total) * 100

    # prints out info
    print("Percentage of ridership for the", user_input, "station: ")
    print(" Weekday ridership:", f"{weekday:,}", f"({percentWeekday:.2f}%)")
    print(" Saturday ridership:", f"{saturday:,}", f"({percentSaturday:.2f}%)")
    print(" Sunday/holiday ridership:", f"{sunHoliday:,}", f"({percentSunHoli:.2f}%)")
    print(" Total ridership:", f"{total:,}")

#######################################################################################################
#
# Command 2:
# Given a connection to the database, find the percentage of riders on weekdays, on Saturdays, and on
# Sundays/holidays for that station based on user input.

def command2(dbConn):
    dbCursor = dbConn.cursor()
    print()

    # gets total ridership grouped by either holiday/sunday ridership, weekday ridership, or saturday ridership
    user_input = input("Enter the name of the station you would like to analyze: ")
    sql = """ SELECT Sum(Num_Riders) from Ridership inner join Stations on 
    Stations.Station_ID = Ridership.Station_ID where Station_Name == ? group by Type_of_Day;"""
    dbCursor.execute(sql, [user_input])
    result = dbCursor.fetchall()

    # if no station exists, command ends
    if not result:
        print("**No data found...")
        print()
        return

    #This query gets the grand total of all 3 categories - this is used for the grand total to figure out percentages
    sql2 = """ SELECT sum(Num_Riders) from Ridership inner join Stations on 
    Stations.Station_ID = Ridership.Station_ID where Station_Name == ?;"""
    dbCursor.execute(sql2, [user_input])
    result2 = dbCursor.fetchall()

    #prints out info
    printAndMathForCommand2(result, result2, user_input)
    print()
    
#######################################################################################################

# printAndMathForCommand3:
# given 2 lists, one that contains the grand total count and the other categorical count totals, prints out the stats
# for command 3 and its percentages

def printAndMathForCommand3(result, result2):
    tempList = [row[0] for row in result2]
    total = int(tempList[0])
    tempList2 = [[row[0], row[1]] for row in result]

    #does math for percentages and prints out stats
    for el in tempList2:
        value = el[1]  
        indvTotals = value / total * 100
        print(f"{el[0]} : {el[1]:,} ({indvTotals:.2f}%)")

#######################################################################################################

# Command 3:
# Given a connection to the database, outputs the total ridership on weekdays for each station, 
# with station names rather than Station IDs as well as their percentages from the grand total of ridership.

def command3(dbConn):
    dbCursor = dbConn.cursor()
    print("Ridership on Weekdays for Each Station")

    # gets totals of ridership by Station Name
    sql = """ SELECT Station_Name, Sum(Num_Riders) As Total from Ridership inner join Stations on Stations.Station_ID = Ridership.Station_ID where Type_of_Day == 'W' 
    group by Station_Name order by Total desc; """
    dbCursor.execute(sql)
    result = dbCursor.fetchall()

    # gets grand total ridership - used for percentages
    sql2 = """ Select Sum(Num_Riders) As Total from Ridership where Type_of_Day == 'W';"""
    dbCursor.execute(sql2)
    resultTotal = dbCursor.fetchall()

    # prints stats
    printAndMathForCommand3(result, resultTotal)
    print()

#######################################################################################################

#printCommand4: 
# Prints stats for command 4 

def printCommand4(result):
    for row in result:
        stop_name = row[0]    
        direction = row[1]             
        ada = row[2]

        # checks for handicap requirement for printing purposes
        if ada == 1:
            print(f"{stop_name} : direction = {direction} (handicap accessible)")
        else:
            print(f"{stop_name} : direction = {direction} (not handicap accessible)")

#######################################################################################################

# Command 4:
# Given a database connection, output all the stops for that line color in that direction as well 
# if they are ADA accessible through user specified line color and direction. Order by stop name in ascending order. 
# The line color and direction should be treated as case-insensitive. 

def command4(dbConn):
    dbCursor = dbConn.cursor()
    print()

    #gets line color results
    user_input = input("Enter a line color (e.g. Red or Yellow): ")
    sql = """SELECT Color from Lines where Color like ?"""
    dbCursor.execute(sql, [user_input])
    result = dbCursor.fetchall()
    
    # if no line exists, then command ends
    if not result:
        print("**No such line...")
        print()
        return

    # gets direction and ADA results
    user_input2 = input("Enter a direction (N/S/W/E): ")
    sql2 = """ SELECT Stop_Name, Direction, ADA from Lines JOIN StopDetails ON Lines.Line_ID = StopDetails.Line_ID JOIN Stops ON StopDetails.Stop_ID = Stops.Stop_ID JOIN Stations ON Stations.Station_ID = Stops.Station_ID where Color like ? and Direction like ? order by Stop_Name asc;"""
    dbCursor.execute(sql2, [user_input, user_input2])
    result2 = dbCursor.fetchall()

    # if no direction exists for specific stop, then command ends
    if not result2:
        print("**That line does not run in the direction chosen...")
        print()
        return

    #prints stats    
    printCommand4(result2)
    print()

#######################################################################################################

# printAndMathForCommand5 
# Prints stats from Command 5 and its percentages associated with the grand total of stops

def printAndMathForCommand5(result, result2):
    tempList = [row[0] for row in result]
    total = int(tempList[0])
    
    for row in result2:
        color = row[0]
        direction = row[1]
        value = row[2]
        indvTotals = row[2] / total * 100
        print(f"{color} going {direction} : {value}", f"({indvTotals:.2f}%)")

#######################################################################################################

# Command 5:
# Given a database connection, output the number of stops for each line color, separated by direction. 
# Show the results in ascending order by color name, and then in ascending order by direction. Also show
# the percentage for each one, which is taken out of the total number of stops.

def command5(dbConn):
    dbCursor = dbConn.cursor()

    print("Number of Stops For Each Color By Direction")

    # gets grand total of stops - used for percentages
    sql = """SELECT count(Stop_ID) from Stops"""
    dbCursor.execute(sql)
    result = dbCursor.fetchall()

    # gets total of stops by color
    sql2 = """SELECT Color, Direction, count(Stops.Stop_ID) from Lines JOIN StopDetails ON Lines.Line_ID = StopDetails.Line_ID JOIN Stops ON StopDetails.Stop_ID = Stops.Stop_ID JOIN Stations ON Stations.Station_ID = Stops.Station_ID group by Color, Direction order by Color, Direction asc;"""
    dbCursor.execute(sql2)
    result2 = dbCursor.fetchall()

    # print stats
    printAndMathForCommand5(result, result2)

#######################################################################################################
# printingForCommand6:
# Prints stats for Command 6
def printingForCommand6(result):
    for row in result:
        year = row[0]
        ridership = row[1]
        print(f"{year} : {ridership:,}")

#######################################################################################################

# plottingForCommand6:
# Plots the data points where x is the years and y is the counts of ridership.
# The plots are saved and named according to their station. I wanted to be able to create plots that didn't override each
# other if the user asked for many plots without exiting the program, so that is why they are named by the station.

def plottingForCommand6(stationName, result):
    x = []
    y = []

    for row in result:
        x.append(row[0])
        y.append(row[1])

    plt.xlabel("Year")
    plt.ylabel("Number of Riders")
    plt.title(f"Yearly Ridership at {stationName} station")

    plt.plot(x, y)
    plt.xticks(x, fontsize=6)
    plt.yticks(fontsize=6)

    plt.ticklabel_format(style='scientific', axis='y', scilimits=(6,6))
    plt.savefig("Command_6_"+stationName+"_plot.png") 
    plt.close()

#######################################################################################################

# Command 6:
# Given a database connection, output the total ridership for each year for that station, in
# ascending order by year, given user specified station.

def command6(dbConn):
    print()
    dbCursor = dbConn.cursor()

    # Gets ridership for each year of user input station
    user_input = input("Enter a station name (wildcards _ and %): ")
    sql = """Select strftime('%Y', Ride_Date) as Year, sum(Num_Riders) from Ridership inner join Stations on Stations.Station_ID = Ridership.Station_ID where Station_Name like ? group by Year Order by Year asc;"""
    dbCursor.execute(sql, [user_input])
    result = dbCursor.fetchall()

    # checks if there is too many stations or no station at all - if function below comes back false, program goes
    # back to user loop
    resultMany = manyStationsInput(dbConn, user_input)
    if not manyStationCheck(resultMany):
        return
    
    # prints stats
    _, station = resultMany[0]
    print("Yearly Ridership at", station)
    printingForCommand6(result)
    print()
    
    # asks for plots - if yes, then plots data
    user_input2 = input("Plot? (y/n) ")
    if user_input2 == "y":
        plottingForCommand6(station, result)
    print()

#######################################################################################################

# printingForCommand7:
# prints stats for command 7
def printingForCommand7(station, year, result):
    print("Monthly Ridership at", station, "for", year)
    for row in result:
        year = row[0]
        month = row[1]
        totals = row[2]
        print(f"{month}/{year} : {totals:,}")

#######################################################################################################

# plottingForCommand7:
# plots the data points where x are the months and y are the ridership counts. 
# The plots are saved and named according to their station and year. I wanted to be able to create plots that didn't override each
# other if the user asked for many plots without exiting the program, so that is why they are named by the station and year.

def plottingForCommand7(stationName, year, result):
    x = []
    y = []
    for row in result:
        x.append(row[1])
        y.append(row[2])

    plt.xlabel("Month")
    plt.ylabel("Number of Riders")
    plt.title(f"Monthly Ridership at {stationName} Station ({year})")

    plt.plot(x, y)
    plt.tight_layout()
    plt.savefig("Command_7_"+stationName+"_"+year+"_plot.png") 
    plt.close()

#######################################################################################################

# Command 7: 
# Given a database connection, output the total ridership for each month in that year given 
# a user specified station and year.

def command7(dbConn):
    print()
    dbCursor = dbConn.cursor()

    # checks too see if there is no station or too many stations in the list
    user_inputStation = input("Enter a station name (wildcards _ and %): ")
    resultMany = manyStationsInput(dbConn, user_inputStation)
    if not manyStationCheck(resultMany):
        return
    
    # gets ridership for each month from said year and station from user input 
    _,stationName = resultMany[0]
    user_inputDate = input("Enter a year: ")
    sql2 = """SELECT strftime('%Y', Ride_Date) as Year, strftime('%m', Ride_Date) as Month, sum(Num_Riders) from Ridership inner join Stations on Stations.Station_ID = 
    Ridership.Station_ID where Station_Name like ? and Year == ? group by Month Order by Month asc"""
    dbCursor.execute(sql2, [user_inputStation, user_inputDate])
    results = dbCursor.fetchall()

    # prints stats
    printingForCommand7(stationName, user_inputDate, results)
    print()

    # plots data if user asks for it
    user_input2 = input("Plot? (y/n) ")
    if user_input2 != "y":
        print()
        return
    else:
        plottingForCommand7(stationName, user_inputDate, results)
    print()

#######################################################################################################

# sqlQueryForStationCommand8:
# Retrieves daily ridership data for a given station and year 

def sqlQueryForStationCommand8(year, station):
    dbCursor = dbConn.cursor()
    sqlStation = """ SELECT Station_Name, Ridership.Station_ID, date(Ride_Date), sum(Num_Riders) from Ridership inner join Stations on 
    Ridership.Station_ID = Stations.Station_ID where strftime('%Y', Ride_Date) == ? and Station_Name like ? group by Ride_Date"""
    dbCursor.execute(sqlStation, [year, station])
    resultStation = dbCursor.fetchall()
    return resultStation

#######################################################################################################

# printingForCommand8:
# Prints stats for command 8
def printingForCommand8(result, result2):
    count = 0
    count2 = 0
    station, stationID,_,_ = result[0]
    station2, stationID2,_,_ = result2[0]

    # station 1 stats
    print("Station 1:", stationID, station)
    for index, row in enumerate(result):
        date = row[2]
        ridership = row[3]
        if index < 5:
            print(f"{date} {ridership}")
        if index >= len(result) - 5:
            print(f"{date} {ridership}")

    # station 2 stats
    print("Station 2:", stationID2, station2)
    for index, row in enumerate(result2):
        date = row[2]
        ridership = row[3]
        if index < 5:
            print(f"{date} {ridership}")
        if index >= len(result2) - 5:
            print(f"{date} {ridership}")
            
#######################################################################################################

# plottingForCommand8:
# Plots data points for 2 different stations where x are the days and y are the ridership totals for each day. 
# The plots are saved and named according to their stations. I wanted to be able to create plots that didn't override each
# other if the user asked for many plots without exiting the program, so that is why they are named by the stations.

def plottingForCommand8(result, result2, year, station1, station2):
    x = []
    y = []
    y2 = []
    for row in result:
        y.append(row[3])
    for row in result2: 
        y2.append(row[3])
    x = list(range(len(y)))

    plt.xlabel("Day")
    plt.ylabel("Number of Riders")
    plt.title(f"Ridership Each Day of {year}")

    plt.plot(x, y, label = station1)
    plt.plot(x, y2, label = station2)
    plt.legend()

    plt.tight_layout()
    plt.savefig("Command8_"+station1+"_VS_"+station2+".png")
    plt.close()

#######################################################################################################

# Command 8:
# Given a database connection, outputs total daily ridership for two user-specified stations in a 
# user-specified year.

def command8(dbConn):
    print()
    dbCursor = dbConn.cursor()

    user_inputYear = input("Year to compare against? ")
    print()

    # checks for station 1 - if there is too many station matches or no station matches
    user_inputStation1 = input("Enter station 1 (wildcards _ and %): ")
    resultManyStation1 = manyStationsInput(dbConn, user_inputStation1)
    if not manyStationCheck(resultManyStation1):
        return
    print()

    # checks for station 2 - if there is too many station matches or no station matches
    user_inputStation2 = input("Enter station 2 (wildcards _ and %): ")
    resultManyStation2 = manyStationsInput(dbConn, user_inputStation2)
    if not manyStationCheck(resultManyStation2):
        return
    
    # gets lists for each station ridership totals
    resultsStation1 = sqlQueryForStationCommand8(user_inputYear, user_inputStation1)
    resultsStation2 = sqlQueryForStationCommand8(user_inputYear, user_inputStation2)

    # prints stats
    printingForCommand8(resultsStation1, resultsStation2)
    print()

    # plots data if asked by user
    station,_,_,_ = resultsStation1[0]
    station2,_,_,_ = resultsStation2[0]
    user_input2 = input("Plot? (y/n) ")
    if user_input2 != "y":
        print()
        return
    else:
        plottingForCommand8(resultsStation1, resultsStation2, user_inputYear, station, station2)
    print()

#######################################################################################################

# pritningForCommand9:
# Prints stats for command 9
def pritningForCommand9(result):
    print()
    print("List of Stations Within a Mile")
    for row in result:
        print(f"{row[0]} : ({row[1]}, {row[2]})")

#######################################################################################################

# plottingForCommand9:
# plots data points where x are longitude points and y are latitude points. The functions plots these data points 
# on a map of Chicago and annotates which point belongs to whatever station associated with said data points.
# The plots are saved and named according to their latitude and longitude. 
# I wanted to be able to create plots that didn't override each
# other if the user asked for many plots without exiting the program, 
# so that is why they are named by the coordinate points.

def plottingForCommand9(results, latitude, longitude):
    x = []
    y = []
    
    for row in results:
        y.append(row[1])  
        x.append(row[2])  

    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] 
    plt.imshow(image, extent=xydims)

    plt.title("Stations Near You")
    plt.plot(x, y, 'o', markersize=5, color='blue') 

    # annotations of each station per their coordinates
    for row in results:
        plt.annotate(row[0], (row[2], row[1]))
    plt.xlim([-87.9277, -87.5569])  
    plt.ylim([41.7012, 42.0868]) 
    plt.savefig("Command9"+ str(longitude)+ ","+ str(latitude)+".png")
    plt.close()

#######################################################################################################

# command 9:
# Given a database connection, output all stations within a mile square radius of a user specified longitude and 
# latitude points. 
def command9(dbConn):
    dbCursor = dbConn.cursor()
    print()

    #checks out of bounds for latitude and longitude points
    user_latitude = float(input("Enter a latitude: "))
    if user_latitude >= 40 and user_latitude <= 43:
        pass
    else:
        print("**Latitude entered is out of bounds...")
        print()
        return

    user_longitude = float(input("Enter a longitude: "))
    if user_longitude >= -88 and user_longitude <= -87:
        pass
    else:
        print("**Longitude entered is out of bounds...")
        print()
        return

    # gets stations near said coordinate points
    sql = """
    SELECT Distinct Station_Name, Latitude, Longitude
    FROM Stops 
    INNER JOIN Stations ON Stops.Station_ID = Stations.Station_ID
    WHERE ABS(Latitude - ?) <= .014 AND ABS(Longitude - ?) <= .02 order by Station_Name asc;"""
    dbCursor.execute(sql, [user_latitude, user_longitude])

    # checks to see if stations exist
    results = dbCursor.fetchall()
    if not results:
        print("**No stations found...")
        print()
        return

    # prints stats and plots data if user asked for it
    pritningForCommand9(results)
    print()

    user_input2 = input("Plot? (y/n) ")
    if user_input2 != "y":
        print()
        return
    else:
        plottingForCommand9(results, user_latitude, user_longitude)
    print()
#######################################################################################################

# user_loop:
# Main driver function that has all the command calls. User is asked to pick a command. Once command is picked,
# the loop calls the user specified command.

def user_loop(dbConn, command):
    dbCursor = dbConn.cursor()
    command = input("Please enter a command (1-9, x to exit): ")
    while command != "x":
        if command == "1":
            command1(dbConn)
        elif command == "2":
            command2(dbConn)
        elif command == "3":
            command3(dbConn)
        elif command == "4":
            command4(dbConn)
        elif command == "5":
            command5(dbConn)
        elif command == "6":
            command6(dbConn)
        elif command == "7":
            command7(dbConn)
        elif command == "8":
            command8(dbConn)
        elif command == "9":
            command9(dbConn)
        else:
            print("**Error, unknown command, try again...")
        command = input("Please enter a command (1-9, x to exit): ")
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
command = ""

# main calls
print_stats(dbConn)
user_loop(dbConn, command)
#
# done
#


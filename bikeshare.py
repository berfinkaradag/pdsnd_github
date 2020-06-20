import pandas as pd
import numpy as np
import time
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


#confirmation funciton will confirm after user makes all entries.
def confirmation_control(): 
    
    while True: 
        confirmation = input("Please confirm your inputs.Type 'yes' to continue and 'no' to restart: \n").strip().lower()
        if confirmation not in ("yes", "no"):
            print("\nInvalid input! Please enter a valid option")
            continue
        elif confirmation == 'yes':
            break
        else: 
            get_filters()
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! My name is Berfin. Let\'s explore some US bikeshare data with me!')
	print('\nYou will learn about bike share use in Chicago,New York City and Washington!')
	
    
    
#while loop for selecting city from cities list
    while True:       
        city = input("\nPlease select a city (Chicago, New york city, Washington): ").strip().lower()
        cities_list = ['chicago','new york city','washington']
        if city not in cities_list:
            print("\nInvalid input! Please enter a valid option")
            continue
        else:
            print("\nData is loading for: '{}' ".format(city.title()))      
            break
            
#while loop for selecting month from months list
    while True:
        month = input("\nPlease enter a month (January to June) or enter all for see all months: ").strip().lower()
        months_list = ['january','february','march','april', 'may', 'june', 'all']
        if month not in months_list:
            print("\nInvalid input! Please enter a valid option")
            continue
        else:
            print("\nData is filtered by: '{}' ".format(month.title()))         
            break
            
#while loop for selecting day from days list
    while True:
        day = input("\nPlease enter a day or enter all for see all days: ").strip().lower()
        days_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
        if day not in days_list:
            print("Invalid input! Please enter a valid option")
            continue
        else:
            print("\nData is filtered by: '{}' ".format(day.title()))          
            break

    print("Data is loading according to your inputs...")
    confirmation_control() #confirmation for entries
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    #converting the Start Time column to datetime type and extracting day of week and month from Start Time to create new columns. And filter by month and     date if user did not type "all"
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['Day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #code for the most common month using mode() function
    months_list2= ['January', 'February', 'March', 'April', 'May','June']
    common_months = df['Month'].mode()[0]
    most_common_month = months_list2[common_months-1].title()
    print("The most common month: ",most_common_month)

    #code for the most common day of week using mode() function
    most_common_day = df['Day'].mode()[0]
    print("The most common day of the week: {}".format(most_common_day))

    #code for the most common start hour using mode() function
    most_start_hour = df['Hour'].mode()[0]
    print("The most common start hour:", most_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nThe Most Popular Stations and Trip are loading...\n")
    start_time = time.time()
    
    #code for the most common start station using mode() function
    start_station = df['Start Station'].mode()[0]
    print("The most common start station: {}".format(start_station))
 
    #code for the most common end station using mode() function
    end_station = df['End Station'].mode()[0]
    print("The most common end station: {}".format(end_station))
    
    #code for the most common start and end station combination using mode() function
    combination = (df['Start Station']+ " -- " + df['End Station']).mode()[0]
    print("The most common start and end station combination is: {}".format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nTrip Duration is loading...\n')
    start_time = time.time()

    #code for total travel time( info: 1 day=86400 seconds,1 hour=3600 seconds, 1 minute=60 seconds)
    total_time = df['Trip Duration'].sum()
    total_days = int(total_time//86400)
    total_hours = int((total_time%86400)//3600)
    total_minutes = int(((total_time%86400)%3600)//60)
    total_seconds = int(((total_time%86400)%3600)%60)
        
    print("The total travel time: {} days, {} hours, {} minutes and {} seconds".format(total_days, total_hours, total_minutes, total_seconds))

    #code for average travel time using mean() function
    average_time = df['Trip Duration'].mean()
    avg_time_minutes = int(average_time//60)
    avg_time_seconds = int(average_time%60)
    
    print("The average travel time: {} minutes, {} seconds".format(avg_time_minutes, avg_time_seconds))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    

def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Informations...\n')
    start_time = time.time()

    #Code for counts of user types using value_counts() function
    user_types = df['User Type'].value_counts().to_string()
    print("User types statistics:")
    print(user_types)
    

    #Code for counts of gender(only available Chicago and New York City, not Washington) using value_counts() function
    try:
        gender_statistic = df['Gender'].value_counts().to_string()
        print("\nGender statistics:")
        print(gender_statistic)
    except KeyError:
        print("There is no data of user genders for {}.".format(city.title()))
        

    #Code for oldest person(using min() function), youngest person(using max() funciton) and most common year of birth(only available Chicago and New york      City, not Washinghton) using mode() function
    try:
        oldest_person = str(int(df['Birth Year'].min()))
        print("\nThe oldest person's birth year : {}".format(oldest_person))
        youngest_person = str(int(df['Birth Year'].max()))
        print("The youngest person's birth year: {}".format(youngest_person))
        common_year = str(int(df['Birth Year'].mode()[0]))
        print("The most common birth year is: {}".format(common_year))
    except:
        print("There is not data of birth year for {}.".format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def display_raw_data(df):
    #if user wants to see the data rows and if i is within the upper limit print dataframe 
    raw_input = input("\nDo you want to see raw data? Enter 'yes' or 'no'\n").strip().lower()    
    if raw_input not in ("yes"):
         print("\nInvalid input! Please enter a valid option")
         display_raw_data(df)
    else:       
        index=0
  
        while True:             
            print(df.iloc[index:index+5,:]) 
            index=index+5
            more_rows = input("\nDo you want to see 5 more rows? Enter 'yes' or 'no'\n").strip().lower()
            if more_rows not in ("yes"):
                break    
                
            if (len(df.index) - 1 < index + 5): 
                print(df.iloc[index:len(df.index)])
                print("Sorry! You reached end of the rows.")
                break
     
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)
        #code for restart the program
        restart = input('\nDo you want to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    
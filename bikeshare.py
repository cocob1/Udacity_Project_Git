import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the city you wish to analyse (Chicago, New York City, Washington):").lower()
    while CITY_DATA.get(city) is None:
        print('Sorry, we couldn\'t find that city.')
        city = input("Please try again (Chicago, New York City, Washington):").lower()
    
    print("Great! You will get informations about {}!".format(city.title()))
    
    # get user input for month (all, january, february, ... , june)
    month = input("Do you want to analyse only one month? Then enter 'Jan', 'Feb', 'Mar', 'Apr','May' or 'Jun'. If you want to analyse all months, type 'all':").lower()
    while month not in ['jan', 'feb', 'mar', 'apr','may', 'jun','all']:
        print('Sorry, we couldn\'t find that month.')
        month = input("Please try again ('Jan', 'Feb', 'Mar', 'Apr','May' or 'Jun'):").lower()
    
    print("Great! You will get informations about {}!".format(month).title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Do you want to analyse only one day of week? Then enter 'Mon', 'Tue', 'Wed', 'Thu','Fri', 'Sat' or 'Sun'. If you want to analyse all days of the week, type 'all':").lower()
    print(month)
    while day not in ['mon', 'tue', 'wed', 'thu','fri', 'sat', 'sun','all']:
        print('Sorry, we couldn\'t find that day. Did you spell it correctly?')
        day = input("Please try again ('Mon', 'Tue', 'Wed', 'Thu','Fri', 'Sat', 'Sun' or 'all''):").lower()
 
    print("Great! You will get informations about {}!".format(day.title()))

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        # filter by month to create the new dataframe
        df = df[(df['month']==months.index(month)+1)]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['mon','tue','wed','thu','fri','sat','sun']
        df = df[(df['day_of_week']==days.index(day))]
        
    #print(df.head())
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month=='all':
        months=['january','february','march','april','may','june']
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]    
        print(popular_month)
        print('The most frequent month for travelling is {}.'.format(months[popular_month-1].title()))
    else:
        print('You filtered data for {}, so that\'s the most common month in the dataset.'.format(month.title()))

    # display the most common day of week
    if day=='all':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        df['dayofweek'] = df['Start Time'].dt.dayofweek
        popular_day = df['dayofweek'].mode()[0]    
        print('The most frequent day of week for travelling is {}.'.format(days[popular_day].title()))
    else:
        print('You filtered data for {}, so that\'s the most common day of week in the dataset.'.format(day.title()))
                  
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]    
    print('The most frequent start hour for travelling is {} o\'clock.'.format(popular_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is {}.'.format(popular_start_station))
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is {}.'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['route']='from ' + df['Start Station'] + ' to ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('The most popular route is {}.'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60
    print('The total travel time is {} hours.'.format(total_travel_time))
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('The mean travel time is {} minutes.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types)
    print('\n')
    
    # Display counts of gender
    try:
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)
    
        # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        
        print('The earliest year of birth is {}.'.format(earliest))
        print('The most recent year of birth is {}.'.format(recent))
        print('The most common year of birth is {}.'.format(common))
    except KeyError:
        print('There is no data available for statistics about gender and birth years.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    show_data = input('Do you want to see individual trip data according to your filter? (Type yes or no):')
    start_row=0
    print(show_data)
    while show_data == 'yes' and start_row<=df['Start Time'].size:
        for row in range(start_row,start_row+5):
            try:
                print('Data from line {}:'.format(row+1))
                print(df.iloc[row])
                print('\n')
            except IndexError:
                print('No more data available.')
                break
        start_row+=5
        if start_row>=df['Start Time'].size:
            break
        else:
            show_data = input('Do you want to see more individual trip data according to your filter? (Type yes or no):')
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

import datetime
import calendar
import time
import pandas as pd
import numpy as np
import re
import math
import matplotlib.pyplot as plt
from pathlib import Path

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

OUT = Path(__file__).resolve().parent/"out"
OUT.mkdir(exist_ok=True)


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
    city = ''
    while(True):
        city = input("Enter the name of the city you want to explore (chicago, new york city, washington): \n")
        city = city.lower().strip()
        possible_city = {r'new york( city)?':'new york city', r'chicago':'chicago', 
                         r'washington( city)?': 'washington'}

        flag = False
        for pos_city, norm_city in possible_city.items():
            if(re.fullmatch(pos_city, city)):
                city = norm_city
                flag = True
                break
        if (flag):
            break
        else:
            print("Oops.. It seems that we don't provide our services in city '{}'!".format(city))
            print("Try to enter one of the three given cities again\n")

    # get user input for month (all, january, february, ... , june)
    month = ''
    while(True):
        month = input("Enter a month you want to get data on (all, january, february...): \n")
        month = month.lower().strip()
        possible_months = {r'all( months)?': 'all', r'jan(uary)?|([0]?1)':'january', r'feb(ruary)?|([0]?2)':'february', r'mar(ch)?|([0]?3)':'march',
                           r'apr(il)?|([0]?4)':'april', r'may|([0]?5)':'may', r'jun(e)?|([0]?6)':'june'}
        
        flag = False
        for pos_mon,norm_mon in possible_months.items():
            if(re.fullmatch(pos_mon, month)):
                month = norm_mon
                flag = True
                break
        if(flag):
            break
        else:
            print("Oops.. There is no such month as {}!".format(month))
            print("Please enter a month from January to June inclusive (you can enter in int format [1,2,...])!\n")     

    # get user input for day of week (all, monday, tuesday, ... sunday)
    dow = ''
    while(True):
        dow = input("Enter a day of the week you want to get a data on (all, monday, tuesday,): \n")
        dow = dow.lower().strip()
        possible_dow = {r'all( days)?':'all', r'mon(day)?|([0]?1)':'monday', r'tue(sday)?|([0]?2)':'tuesday', 
                            r'wed(nesday)?|([0]?3)':'wednesday',r'thu(rsday)?|([0]?4)':'thursday', r'fri(day)?|([0]?5)':'friday',
                            r'sat(urday)?|([0]?6)':'saturday', r'sun(day)?|([0]?7)':'sunday'}
        
        flag = False
        for pos_dow, norm_dow in possible_dow.items():
            if(re.fullmatch(pos_dow, dow)):
                dow = norm_dow
                flag = True
                break
        if(flag):
            break
        else:
            print("Oops.. There is no such day as {}!".format(dow))
            print("Please enter a day from Monday to Sunday inclusive (you can enter in int format [1,2,...])\n")

    print('-'*40)
    return city, month, dow


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
    global CITY_DATA
    MONTHS = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6,
              'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    DAYS = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
    
    df = pd.read_csv(f'./{CITY_DATA[city]}', parse_dates=['Start Time', 'End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if(month!='all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    
    if(day!='all'):
        days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
        df = df[df['day_of_week'] == days[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"Most common month: {calendar.month_name[df['Start Time'].dt.month.mode()[0]]}") 

    # display the most common day of week
    print(f"Most common day of week: {calendar.day_name[df['Start Time'].dt.dayofweek.mode()[0]]}")

    # display the most common start hour
    print(f"Most common start hour: {df['Start Time'].dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used start station: {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"Most commonly used end station: {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    df['Start-End Stations'] = df['Start Station'] + '-->' + df['End Station']
    print(f"Most frequent combination of start station and end station trip: {df['Start-End Stations'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = str(datetime.timedelta(seconds=int(df['Trip Duration'].sum())))
    h_min_sec_time = total_time.split(',')[-1].split(':')
    print(f"Total travel time: {total_time.split(',')[0]},{h_min_sec_time[0]} hours, \
{h_min_sec_time[1]} minutes, {h_min_sec_time[2]} seconds")

    # display mean travel time
    print(f"Mean travel time (in hours:minutes:seconds): {datetime.timedelta(seconds = int(df['Trip Duration'].mean()))}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types: \n{df['User Type'].value_counts()}\n")

    # Display counts of gender
    print(f"Counts of gender: \n{df['Gender'].value_counts()}\n")

    # Display earliest, most recent, and most common year of birth
    print(f"Earliest year of birth: {df['Birth Year'].min()}")
    print(f"Most recent year of birth: {df['Birth Year'].max()}")
    print(f"Most common year of birth: {df['Birth Year'].mode()[0]}")
    print(f"Mean year of birth: {math.floor(df['Birth Year'].mean())}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def chunker(df, beg, size):
    return df.iloc[beg:beg+size]

def see_head(df):
    choice = input("Do you want to see the first 5 rows? (yes/no): ").strip()
    if(choice.lower()!='yes'):
        return 

    length = len(df.index)
    size = 0
    current_pos = 0
    while(True):
        size = min(length-cur_pos, 5)
        for idx, row in df.iloc[current_pos:current_pos+size].iterrows():
            print('{',f"'':'{idx}'")
            print(f" 'Birth Year': '{row['Birth Year']}'")
            print(f" 'End Station': '{row['End Station']}'")
            print(f" 'Gender': '{row['Gender']}'")
            print(f" 'Start Station': '{row['Start Station']}'")
            print(f" 'Start Time': '{row['Start Time']}'")
            print(f" 'Trip Duration': {row['Trip Duration']}")
            print(f" 'User Type': {row['User Type']}", '}')
        print('\n')
        cur_pos += size
        choice = input(f"...Do you want to see next {min(length-cur_pos, 5)} rows? (yes/no): ")
        if(choice.lower()!='yes'):
            return
        print('\n', '.'*10, '\n')

def compare_frequency():
    """Creates a plot with three graphs with the comparison of mean of rentals number per 7 day window 
       for three cities during the whole given period of time (Jan - Jun)"""
    
    chicago = pd.read_csv('./chicago.csv', usecols=['Start Time'], parse_dates=True)
    new_york = pd.read_csv('./new_york_city.csv',usecols=['Start Time'], parse_dates=True)
    washington = pd.read_csv('./washington.csv', usecols=['Start Time'], parse_dates=True)

    chicago_daily = pd.to_datetime(chicago['Start Time']).dt.floor("D").value_counts().sort_index()
    new_york_daily = pd.to_datetime(new_york['Start Time']).dt.floor("D").value_counts().sort_index()
    washington_daily = pd.to_datetime(washington['Start Time']).dt.floor("D").value_counts().sort_index()

    full_chicago = pd.date_range(chicago_daily.index.min(), chicago_daily.index.max(), freq='D')
    full_new_york_daily = pd.date_range(new_york_daily.index.min(), new_york_daily.index.max(), freq='D')
    full_washington = pd.date_range(washington_daily.index.min(), washington_daily.index.max(), freq='D')

    chicago_daily = chicago_daily.reindex(full_chicago, fill_value=0)
    new_york_daily = new_york_daily.reindex(full_new_york_daily, fill_value=0)
    washington_daily = washington_daily.reindex(full_washington, fill_value=0)

    plt.figure()    

    plt.plot(chicago_daily.rolling(7, min_periods=1).mean())
    plt.plot(new_york_daily.rolling(7, min_periods=1).mean())
    plt.plot(washington_daily.rolling(7, min_periods=1).mean())

    plt.legend(['Chicago', 'New York City', 'Washington'])
    plt.title("Comparison of the mean of number of rentals per 7 day window")
    plt.savefig(OUT/'rental_count_per_interval.png')

def compare_mean_time():
    """Creates a plot with comparison of median travel time per 7 day window for three cities 
       during the whole given period of time (Jan - Jun)"""
    
    chicago = pd.read_csv('./chicago.csv', usecols=['Trip Duration', 'Start Time'])
    new_york = pd.read_csv('./new_york_city.csv', usecols=['Trip Duration', 'Start Time'])
    washington = pd.read_csv('./washington.csv', usecols=['Trip Duration', 'Start Time'])

    chicago['Start Time'] = pd.to_datetime(chicago['Start Time']).dt.floor('D')
    new_york['Start Time'] = pd.to_datetime(new_york['Start Time']).dt.floor('D')
    washington['Start Time'] = pd.to_datetime(washington['Start Time']).dt.floor('D')

    chicago = chicago.groupby(['Start Time'])['Trip Duration'].median().sort_index().asfreq('D')
    new_york = new_york.groupby(['Start Time'])['Trip Duration'].median().sort_index().asfreq('D')
    washington = washington.groupby(['Start Time'])['Trip Duration'].median().sort_index().asfreq('D')

    plt.figure()    

    plt.plot(chicago.rolling(7, min_periods=2).median())
    plt.plot(new_york.rolling(7, min_periods=2).median())
    plt.plot(washington.rolling(7, min_periods=2).median())

    plt.legend(['Chicago', 'New York City', "Washington"])
    plt.title("Comparison of the median travel time per 7 day window")
    plt.savefig(OUT/'travel_time_per_interval.png')

def hourly_count(df, city, month, day):
    cnt = df.groupby(['hour']).size().reindex(range(24), fill_value=0)
    plt.figure()
    plt.bar(cnt.index, cnt.values)
    mon_title = month.title()
    if(month == 'all'):
        mon_title = 'all available months'
    plt.title(f"Trips by hour in {city.title()} (m={mon_title}, dow={day.title()})")
    plt.xlabel('Hours(0-23)')
    plt.show()

def monthly_count(df, city, month, day, smooth):
    cnt = df['date'].value_counts().sort_index()
    full_range = pd.date_range(cnt.index.min(), cnt.index.max(), freq='D')
    cnt = cnt.reindex(full_range, fill_value = 0)
    plt.figure()
    plt.plot(cnt)
    plt.plot(cnt.rolling(smooth,center=True,min_periods=1).mean())
    plt.legend(['Daily', f'{smooth}-day rolling mean'])

    plt.title(f'Trips per day in {city.title()} (m={month.title()}, dow=all days)')
    plt.ylabel('Trips')
    plt.show()

def draw_interactive(df, city, month, day):
    dt = pd.to_datetime(df['Start Time'])
    df['hour'] = dt.dt.hour
    df['month'] = dt.dt.month
    df['date'] = dt.dt.floor('D')
    if((month == 'all' and day!='all') or (month!='all' and day!='all')):
        hourly_count(df,city,month,day)
    elif(month!=all):
        monthly_count(df, city, month, day, 3)#setting a different smooth parameter so that window won't be too large
    else:
        monthly_count(df, city, month, day, 7)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_head(df)
        compare_freq_choice = input('\nWould you like to rerender the comparison between three cities (you can find it in ./out)? (yes/no): ')
        if(re.fullmatch(r'y(es)?', compare_freq_choice.lower())):
            compare_frequency()
            compare_mean_time()

        draw_interactive_choice = input('\nDo you want to see the graphical representation of your data? (yes/no): ')
        if(re.fullmatch(r'y(es)?', draw_interactive_choice.lower())):
            draw_interactive(df,city,month,day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

cities_dict = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
months_list = ["January", 'February', 'March', 'April', 'May', 'June', 'All']
weekday_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input('You can choose one of the following cities: Chicago, New york city and Washington.\nPlease, enter the city name:\n')
    while city.strip().title() not in cities_dict:
        city = input('Enter a valid city name \n(Chicago, New york city or Washington)\n')

    # get user input for month (all, january, february, ... , june)
    month = input('Now, you will select the time frame of statistics:\nIF you want to select all months enter \"All\" otherwise enter the name of selected month:\n')
    while month.strip().title() not in months_list:
        month = input('Invalid input, enter \"All\" or valid month name \n(january, february, march, april, may or june)\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('And for week day, you can enter \"All\" for no filtration based on week day or you can enter the seclected week day:\n')
    while day.strip().title() not in weekday_list:
        day = input('Invalid input, enter \"All\" or valid week day \n(monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n')

    print('__'*30)
    return city.strip().title(), month.strip().title(), day.strip().title()

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
    # read the csv file of the city
    df = pd.read_csv(cities_dict[city])
    raw_df = pd.read_csv(cities_dict[city])

    # Use start time column to filter the data and convert it into date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday

    # if user enter a month name, make a filteration based on this month
    if month != 'All':
        month = months_list.index(month) + 1
        df = df.loc[df['month'] == month]

    # if user enter a week day name, make a filteration based on this week day
    if day != 'All':
        df = df.loc[df['day'] == weekday_list.index(day)]

    return df, raw_df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        months_count = df['month'].value_counts()
        print('The most common month:', months_list[months_count.idxmax()-1])
        # minus one because max value come from the table data

    # display the most common day of week
    if day == 'All':
        days_count = df['day'].value_counts()
        print('The most common day:', weekday_list[days_count.idxmax()-1])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hours_count = df['hour'].value_counts()
    print('The most common start hour:', hours_count.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('__'*30)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations_count = df['Start Station'].value_counts()
    print('The most popular start station:', start_stations_count.idxmax())

    # display most commonly used end station
    end_stations_count = df['End Station'].value_counts()
    print('The most popular end station:', end_stations_count.idxmax())

    # display most frequent combination of start station and end station trip
    # create a column contain the combination between start station and end stations
    df['Start-End-Stations'] = df['Start Station'] + '+' + df['End Station']
    # calculate the most frequent combination
    df['Start-End-Stations'] = df['Start Station'] + '+' + df['End Station']
    start_end_stations_count = df['Start-End-Stations'].value_counts()
    start_station, end_station = start_end_stations_count.idxmax().split('+')
    print('The most popular combination of start station and end station trip: ({}) with ({})'.format(start_station, end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('__'*30)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in sec and min
    total_sec = df['Trip Duration'].sum()
    print('The total travel time =', total_sec, 'Sec', '=', format(total_sec/60,'.2f'), 'Min')

    # display mean travel time
    mean_sec = df['Trip Duration'].mean()
    print('The mean travel time =', format(mean_sec,'.2f'), 'Sec', '=', format(mean_sec/60,'.2f'), 'Min')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('__'*30)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('The counts of user types:\n', user_types_count, '\n')

    # Display counts of gender
    if city != 'Washington':
        gender_count = df['Gender'].value_counts()
        print('The counts of gender:\n', gender_count, '\n')

    # Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        print('The earlist year of birth:', df['Birth Year'].min())
        print('The most recent year of birth:', df['Birth Year'].max())
        birth_year_count = df['Birth Year'].value_counts()
        print('The most common year of birth:', birth_year_count.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('__'*30)


def display_raw_data(raw_df):
    """Ask user if want to see the first five rows of raw data and ask him if want to see more rows"""

    show_data = input('Are you want to see the first five rows of raw data? If you want, please enter "yes" otherwise enter "no" \n')
    # define iterate parameter i
    i = 0
    # define break_state variable that we will use to break the while loop
    break_state = 'no'
    # while loop will print the first five rows of raw data and break when user doesn't need more or all raw data has been printed
    while show_data.strip().title() == 'Yes':
        # print the five rows
        for j in range(5):
            # check if the iteration parameter exceed the number of rows
            if (i+j) < raw_df.shape[0]-1:
                print(raw_df.loc[i+j])
            else:
                # break if exceed the limit and make parameter break_state to break the while loop
                break_state = "break"
                break
        # if exceed the limit in for loop, break the while loop
        if break_state == 'break':
            break
        show_data = input('Are you want to see more five rows of raw data?  If you wan\'t, please enter "yes" otherwise enter "no" \n')
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df, raw_df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(raw_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

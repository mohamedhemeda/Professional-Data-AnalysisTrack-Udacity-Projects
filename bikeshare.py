import time
import calendar
import pandas as pd
import numpy as np
pd.set_option('expand_frame_repr', False)  # to show data frame rows in single line
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS_OF_WEEK = {1: 'sunday',
                2: 'monday',
                3: 'tuesday',
                4: 'wednesday',
                5: 'thursday',
                6: 'friday',
                7: 'saturday'}
filter_type = ['none', 'month', 'day', 'both']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cites = []
    for key in CITY_DATA:
        cites.append(key)
    # print(cites)
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = str(input("Choose City You Want To Analyze  from (chicago, new york city, washington)Please "))
    if city_input.lower() in cites:
        city = CITY_DATA[city_input.lower()]  # to pass the name of file directly to load_data function

    while city_input.lower() not in cites:
        print("Please Enter Valid City")
        city_input = str(input("Choose City You Want To Analyze  from (chicago, new york city, washington)Please "))
        if city_input.lower() in cites:
            city = CITY_DATA[city_input.lower()]
    # TO DO: get user input for month (all, january, february, ... , june)

    user_filter = str(input("Would You like To Filter by (month , day , both or no filter) Note:if no type :none "))
    while user_filter.lower() not in filter_type:
        print("Please Enter Valid filter")
        user_filter = str(input("Would You like To Filter by (month , day , both or no filter) Note:if no type :none "))
    if user_filter == 'month':
        month = str(input("Enter Month between" + str(months) + "Filter: " + user_filter))
        if month in months:
            print("this month endswith " + str(calendar.monthrange(2017, months.index(month)+1)[1]) + "days")
        while month not in months:
            print("Enter Valid Month")
            month = str(input("Enter Month between" + str(months) + "Filter: " + user_filter))
            if month in months:
                print("this month endswith " + str(calendar.monthrange(2017, months.index(month) + 1)[1]) + "days")
        day = 'all'
    elif user_filter == 'day':
        month = 'all'
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = int(input("pleas Enter your Favourite day  " + "Filter: " + user_filter))
                while day > 7 or day < 1:
                    print("pleas enter day between 1 and 7 ")
                    day = int(input("pleas Enter your Favourite day  " + "Filter: " + user_filter))
                break
            except ValueError:
                print("Not an integer! Try again. or invalid day")
            except KeyboardInterrupt:
                print("\nNo Input Taken")
                break
            finally:
                print("Lets go to the next steps: ")

    elif user_filter == 'both':
        month = str(input("Enter Month between" + str(months) + "Filter: " + user_filter))
        while month not in months:
            print("Enter Valid Month")
            month = str(input("Enter Month between" + str(months) + "Filter: " + user_filter))
        if month in months:
            print("this month endswith " + str(calendar.monthrange(2017, months.index(month) + 1)[1]) + " days")
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = int(input("pleas Enter your Favourite day  " + "Filter: " + user_filter))
                if month in months:
                    print("this month endswith " + str(calendar.monthrange(2017, months.index(month) + 1)[1]) + " days")
                while day > 7 or day < 1:
                    print("pleas enter day between 1 and 7 ")
                    day = int(input("pleas Enter your Favourite day  " + "Filter: " + user_filter))
                    if month in months:
                        print("this month endswith " + str(
                            calendar.monthrange(2017, months.index(month) + 1)[1]) + " days")
                break
            except ValueError:
                print("Not an integer! Try again. or invalid day")
            except KeyboardInterrupt:
                print("\nNo Input Taken")
                break
            finally:
                print("Lets go to the next steps: ")

    # Notice: there is another way to get the year according to the file:
    # 1-  read csv file.  2- store file in data frame.   3- convert the coloum startTime to to_datetime
    # 4- extract year from this coloum using df['starTime'].dt.year to make it general or read it from user
    # calendar.monthrange() is used because there is month like february 28 or 29 days if user enter 30
    elif user_filter == 'none':
        month = 'all'
        day = 'all'

    print('-' * 40)
    return city, month, day, user_filter


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
    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['week_days'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['total_trip'] = "(" + df['Start Station'] + ")" + " and (" + df['End Station'] + ")"
    if month != 'all':
        # filter by month to create the new dataframe
        this_month = months.index(month) + 1  # because starts from 0
        df = df[df['month'] == this_month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_days'] == DAYS_OF_WEEK[day].title()]

    return df


def time_stats(df, user_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts()[popular_month]
    popular_week_days = df['week_days'].mode()[0]
    popular_week_days_count = df['week_days'].value_counts()[popular_week_days]
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts()[popular_hour]

    if user_filter == 'both':
        print("The most popular_hour is :" + str(popular_hour) + " count = " + str(popular_hour_count) +
              "Filter: " + user_filter)
    elif user_filter == 'month':
        print("The most popular_week of day is :" + str(popular_week_days) + " count = " +
              str(popular_week_days_count) + "   The most popular_hour is :" + str(popular_hour) +
              "  count = " + str(popular_hour_count) + "Filter: " + user_filter)
    elif user_filter == 'day':
        print("The most popular_month is :" + str(popular_month) + " count = " + str(popular_month_count) +
              "    The most popular_hour is :" + str(popular_hour) + " count = " +
              str(popular_hour_count) + "Filter: " + user_filter)
    elif user_filter == 'none':
        print("The most popular_month is :" + str(popular_month) + " count = " + str(popular_month_count) +
              "    The most popular_week of day is :" + str(popular_week_days) + "  count =" +
              str(popular_week_days_count) + "    The most popular_hour is :" +
              str(popular_hour) + " count = " + str(popular_hour_count) + "Filter: " + user_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start = df['Start Station'].mode()[0]     # most common start station
    count_most_start = df['Start Station'].value_counts()[most_start]
    print("The Most Start Station is : " + str(most_start) + "  count = " + str(count_most_start))

    # TO DO: display most commonly used end station

    most_end = df['End Station'].mode()[0]         # most common End station
    count_most_end = df['End Station'].value_counts()[most_end]
    print("The Most Start Station is : " + str(most_end) + " count = " + str(count_most_end))
    # TO DO: display most frequent combination of start station and end station trip
    most_combines = df['total_trip'].mode()[0]
    count_most_combined = df['total_trip'].value_counts()[most_combines]
    print(" The Total Trip  ......")
    print("The Most Combined Stations are : " + str(most_combines) + " count = " + str(count_most_combined))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The Total Travel Time is : " + str(total_travel_time))
    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print("The Average Travel Time is : " + str(average_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("User Types: \n" + str(user_type_counts.to_string()))
    # TO DO: Display counts of gender
    if city != 'washington.csv':
        user_gender = df['Gender'].value_counts()
        print("Gender is :\n" + str(user_gender.to_string()))
    else:
        print("There is no gender data to show")
    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington.csv':
        earliest_birth = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("Earliest Year of Birth is " + str(int(earliest_birth)))
        print("Most Recent Year of Birth is " + str(int(most_recent)))
        print("The Most Common Year of Birth is " + str(int(most_common)))
    else:
        print("There is no Birth Year data to show")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day, user_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, user_filter)
        station_stats(df)
        trip_duration_stats(df)

        user_stats(df, city)

        i = 0
        show_data = input('\nWould you like to show some data? Enter yes or no.\n')

        while show_data.lower() == 'yes' or i >= len(df.index):
            print(df[i:i + 5])
            i += 5
            show_data = input('\nWould you like to show some data? Enter yes or no.\n')
        else:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
    main()

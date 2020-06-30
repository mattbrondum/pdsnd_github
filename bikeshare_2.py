import time
import pandas as pd
import numpy as np

# Note: script currently only includes cities in CITY_DATA dictionary
# if more cities need to be added, just add them to the dictionary below
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Filtering data...')

    # If the user enters more than 10 wrong inputs, exit the script
    wrong_count = 0

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['all', 'chicago', 'new york city', 'washington']

    while True:
        city = str(input('Enter a city: ')).strip().lower()
        if city in valid_cities:
            break
        else:
            wrong_count += 1
            if wrong_count > 5:
                print('Program ending after 10 bad inputs!')
                exit()
            print('Sorry I didn\'t like that city name! Try `Chicago` for example.')
            continue

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    valid_months_abbr = [x[:3] for x in valid_months]
    while True:
        month = str(input('Enter a month: ')).strip().lower()
        if (month in valid_months) or (month in valid_months_abbr):
            break
        else:
            wrong_count += 1
            if wrong_count > 5:
                print('Program ending after 10 bad inputs!')
                exit()
            print('Sorry I didn\'t like that month! Try `February` for example.')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # accepts 3-day abbreviations like Mon, Tues
    valid_days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    valid_days_abbr = [x[:-3] for x in valid_days]
    while True:
        day = str(input('Enter a day of week: ')).strip().lower()
        if day in valid_days:
            break
        elif day in valid_days_abbr:
            day = day + 'day'
            break
        else:
            wrong_count += 1
            if wrong_count > 5:
                print('Program ending after 10 bad inputs!')
                exit()
            print('Sorry I didn\'t like that day of week! Try `Sunday` for example.')
            continue
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    - Adds day of week and month column
    - Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Loading data for...')
    print('City: {}'.format(city))
    print('Month: {}'.format(month))
    print('Day of week: {}'.format(day))
    csv_string = city.replace(' ', '_') + '.csv'
    try:
        df = pd.read_csv(csv_string)
    except:
        print('Error finding csv named {}'.format(csv_string))
        exit()
    # Convert time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['Start Time'])

    # Create month and day column from Time column
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day'] = df['Start Time'].dt.day_name().str.lower()
    df['Hour'] = df['Start Time'].dt.hour


    # Filter based on day and week if necessary
    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]

    print('Analyzing {} trips within that scope...'.format(len(df)))
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (iff there are multiple)
    if month == 'all':
        common_month = df['Month'].value_counts().idxmax()
        print('The most common month is: {}'.format(common_month.title()))

    # display the most common day of week (iff there are multiple)
    if day == 'all':
        common_day = df['Day'].value_counts().idxmax()
        print('The most common day is: {}'.format(common_day.title()))

    # display the most common start hour
    common_hour = df['Hour'].value_counts().idxmax()
    if common_hour < 12:
        print('The most common start time is in the morning at {} AM.'.format(common_hour))
    elif common_hour < 17:
        print('The most common start time is afternoon at {} PM.'.format(common_hour-12))
    else:
        print('The most common start time is at night at {} PM.'.format(common_hour-12))

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most common start station is: {}'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('The most common end station is: {}'.format(common_end_station))

    # display most frequent permutation of start station and end station trips
    start_end_combos = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    common_combo_station = start_end_combos.index[0]
    print('The most frequent start-end combination was starting in {s} and ending in {e}.'.format(s = common_combo_station[0]
                                                                                                  ,e = common_combo_station[1]))

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_time = df['Trip Duration'].sum()
    m, s = divmod(total_time, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('The total time spent on bikes across all trips was {d} days {h} hours {m} minutes {s} seconds'.format(d=d, h=h, m=m, s=s))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    m, s = divmod(mean_time, 60)
    s = int(s)
    print('The average time spent on bikes across all trips was {m}min {s}sec'.format(m=m, s=s))

    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users (where applicable)."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertype_counts = df.groupby('User Type').size()
    print('Trip counts by user type: ')
    print(usertype_counts)

    # Display counts of gender
    if 'Gender' in df.columns.tolist():
        gender_counts = df.groupby('Gender').size()
        print('Trip counts by user gender: ')
        print(gender_counts)
    else:
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.tolist():
        df['Rider Age'] = df['Start Time'].dt.year - df['Birth Year']
        oldest = int(df['Birth Year'].min())
        oldest_yo = int(df['Rider Age'].max())
        print("The oldest user was {} years old, born in {}".format(oldest_yo, oldest))

        youngest = int(df['Birth Year'].max())
        youngest_yo = int(df['Rider Age'].min())
        print("The youngest user was {} years old, born in {}".format(youngest_yo, youngest))

        age_mode = int(df['Birth Year'].mode())
        age_mode_yo = int(df['Rider Age'].mode())
        print("The most common user was {} years old, born in {}".format(age_mode_yo, age_mode))
    else:
        print('No age data available')

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-' * 40)

def raw_data_print(df):
    while True:
        print_raw = input('\nWould you like to see raw data? Enter yes or no.\n')
        if print_raw.lower() == 'no':
            break
        elif print_raw.lower() == 'yes':
            n_lines = int(input('\nHow many lines would you like to see? Enter a number between 1 to 10.\n'))
            if n_lines > 0 & n_lines < 11:
                sample_df = df.sample(n=n_lines)
                for sample_row in sample_df.iterrows():
                    print(sample_row)

        else:
            print("I didn't understand. Let's try again ")
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_print(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

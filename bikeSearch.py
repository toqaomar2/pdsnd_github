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

    # Get user input for city
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Enter the city (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        else:
            print("Invalid input. Please choose from chicago, new york city, or washington.")

    # Get user input for month
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Enter the month to filter by (all, january, february, ... , june): ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose a valid month or 'all'.")

    # Get user input for day of week
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Enter the day of week to filter by (all, monday, tuesday, ... , sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose a valid day or 'all'.")

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

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time'
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print(f"The most common month is: {common_month.title()}")

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of week is: {common_day.title()}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Start-End Combo'] = df['Start Station'] + " to " + df['End Station']
    common_start_end_combo = df['Start-End Combo'].mode()[0]
    print(f"The most frequent combination of start station and end station is: {common_start_end_combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time}")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()

    # Continue showing data as long as the user wants
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])  # Display next 5 rows
        start_loc += 5  # Move to the next batch of rows

        # Ask if the user wants to continue
        if start_loc >= len(df):
            print("You've reached the end of the data.")
            break
        view_data = input("Do you wish to see the next 5 rows of data? Enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Call the new function to display data
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

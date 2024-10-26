import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    print('Hello! Welcome to the US bikeshare data exploration tool!')
    city = input('Which city\'s data would you like to explore: Chicago, New York City, or Washington?\n').strip().lower()
    while city not in CITY_DATA:
        print('Invalid input. Please enter one of the following cities: Chicago, New York City, or Washington.')
        city = input('Which city\'s data would you like to explore: Chicago, New York City, or Washington?\n').strip().lower()

    month = input("Which month would you like to filter by? You can enter a month name (e.g., January) or number (e.g., 1) or type 'all' for no filter:\n").strip().lower()
    while month not in ['all'] + [m[:3] for m in MONTHS] + list(map(str, range(1, 13))):
        print('Invalid input. Please enter a valid month name, number, or "all".')
        month = input("Which month would you like to filter by? You can enter a month name (e.g., January) or number (e.g., 1) or type 'all' for no filter:\n").strip().lower()

    day = input("Which day of the week would you like to filter by? Enter 'all' for no filter, or specify a day (e.g., Monday or Mon):\n").strip().lower()
    while day not in ['all'] + [d[:3] for d in DAYS]:
        print('Invalid input. Please enter a valid day of the week or "all".')
        day = input("Which day of the week would you like to filter by? Enter 'all' for no filter, or specify a day (e.g., Monday or Mon):\n").strip().lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = month[:3]
        if month.isdigit():
            month = MONTHS[int(month) - 1]
        month = month.lower()
        if month in MONTHS:
            df = df[df['Month'] == MONTHS.index(month) + 1]

    if day != 'all':
        day = day[:3].capitalize()
        if day in DAYS:
            df = df[df['Day_of_Week'] == day]

    return df

def time_stats(df):
    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    common_day_of_week = df['Day_of_Week'].mode()[0]
    common_start_hour = df['Hour'].mode()[0]

    print(f'The most common month is: {MONTHS[common_month - 1].title()}.')
    print(f'The most common day of the week is: {common_day_of_week}.')
    print(f'The most common start hour is: {common_start_hour}.')

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def station_stats(df):
    print('\nCalculating the most popular stations and trips...\n')
    start_time = time.time()

    if 'Start Station' in df.columns and 'End Station' in df.columns:
        common_start_station = df['Start Station'].mode()[0]
        common_end_station = df['End Station'].mode()[0]

        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Trip'].mode()[0]

        print(f'The most common start station is: {common_start_station}.')
        print(f'The most common end station is: {common_end_station}.')
        print(f'The most common trip is: {common_trip}.')
    else:
        print('No station data available for this dataset.')

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating trip duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()

        print(f'The total travel time is: {total_travel_time}.')
        print(f'The average travel time is: {mean_travel_time:.2f}.')
    else:
        print('No trip duration data available for this dataset.')

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def user_stats(df):
    print('\nCalculating user statistics...\n')
    start_time = time.time()

    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('Counts of user types:')
        for user_type, count in user_types.items():
            print(f'  {user_type}: {count}')

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:')
        for gender, count in gender_counts.items():
            print(f'  {gender}: {count}')
    else:
        print('No gender data available for this dataset.')

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        
        print(f'The earliest birth year is: {earliest_birth_year}.')
        print(f'The most recent birth year is: {most_recent_birth_year}.')
        print(f'The most common birth year is: {most_common_birth_year}.')
    else:
        print('No birth year data available for this dataset.')

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def display_data(df):
    start_loc = 0
    while input("Would you like to view 5 rows of individual trip data? Enter 'y' for yes or 'n' for no: ").strip().lower() == 'y':
        if start_loc >= len(df):
            print("No more data to display.")
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        if input('\nWould you like to restart? Enter "y" for yes or "n" for no:\n').strip().lower() != 'y':
            break

if __name__ == "__main__":
    main()

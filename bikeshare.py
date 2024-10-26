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
    print('Welcome to the US bikeshare data exploration tool!')
    city = input('Please select a city (Chicago, New York City, Washington):\n').strip().lower()
    while city not in CITY_DATA:
        print('Invalid city. Choose from: Chicago, New York City, Washington.')
        city = input('Please select a city:\n').strip().lower()

    month = input("Select a month (e.g., January) or type 'all' for no filter:\n").strip().lower()
    while month not in ['all'] + [m[:3] for m in MONTHS] + list(map(str, range(1, 13))):
        print('Invalid month. Enter a valid month or "all".')
        month = input("Select a month:\n").strip().lower()

    day = input("Select a day (e.g., Monday) or type 'all' for no filter:\n").strip().lower()
    while day not in ['all'] + [d[:3] for d in DAYS]:
        print('Invalid day. Enter a valid day or "all".')
        day = input("Select a day:\n").strip().lower()

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
    print('\nCalculating the most common travel times...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    common_day_of_week = df['Day_of_Week'].mode()[0]
    common_start_hour = df['Hour'].mode()[0]

    print(f'Most common month: {MONTHS[common_month - 1].title()}.')
    print(f'Most common day of the week: {common_day_of_week}.')
    print(f'Most common start hour: {common_start_hour}.')

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

        print(f'Most common start station: {common_start_station}.')
        print(f'Most common end station: {common_end_station}.')
        print(f'Most common trip: {common_trip}.')
    else:
        print('Station data is not available for this dataset.')

    print(f"\nCalculation completed in {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating trip duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()

        print(f'Total travel time: {total_travel_time}.')
        print(f'Average travel time: {mean_travel_time:.2f}.')
    else:
        print('Trip duration data is not available for this dataset.')

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
        print('Gender data is not available for this dataset.')

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        
        print(f'Earliest birth year: {earliest_birth_year}.')
        print(f'Most recent birth year: {most_recent_birth_year}.')
        print(f'Most common birth year: {most_common_birth_year}.')
    else:
        print('Birth year data is not available for this dataset.')

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

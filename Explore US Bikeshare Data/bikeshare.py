import pandas as pd

# Define the filename for each city's dataset
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def load_data(city):
    """
    Loads data for the specified city.
    
    Args:
        city (str): Name of the city to analyze
        
    Returns:
        DataFrame: Pandas DataFrame containing city data
    """
    try:
        # Load data file into a DataFrame
        df = pd.read_csv(CITY_DATA[city])
        
        # Convert 'Start Time' and 'End Time' columns to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        
        return df
    
    except FileNotFoundError:
        print(f"Error: File for {city.title()} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading data for {city.title()}: {e}")
        return None

def popular_times(df):
    """
    Computes the popular times of travel.
    
    Args:
        df (DataFrame): Pandas DataFrame containing city data
        
    Returns:
        tuple: (most common month, most common day of week, most common hour of day)
    """
    try:
        # Compute the most common month, day of week, and hour of day
        common_month = df['Start Time'].dt.month.mode()[0]
        common_day_of_week = df['Start Time'].dt.dayofweek.mode()[0]
        common_hour_of_day = df['Start Time'].dt.hour.mode()[0]
        
        return common_month, common_day_of_week, common_hour_of_day
    
    except Exception as e:
        print("An error occurred while computing popular times:", e)
        return None, None, None

def popular_stations(df):
    """
    Computes the popular stations and trips.
    
    Args:
        df (DataFrame): Pandas DataFrame containing city data
        
    Returns:
        tuple: (most common start station, most common end station, most common trip)
    """
    try:
        # Compute the most common start and end stations
        common_start_station = df['Start Station'].mode()[0]
        common_end_station = df['End Station'].mode()[0]
        
        # Compute the most common trip (combination of start and end stations)
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Trip'].mode()[0]
        
        return common_start_station, common_end_station, common_trip
    
    except Exception as e:
        print("An error occurred while computing popular stations:", e)
        return None, None, None

def trip_duration(df):
    """
    Computes trip duration statistics.
    
    Args:
        df (DataFrame): Pandas DataFrame containing city data
        
    Returns:
        tuple: (total travel time, average travel time)
    """
    try:
        # Compute total and average travel time
        total_travel_time = df['Trip Duration'].sum()
        average_travel_time = df['Trip Duration'].mean()
        
        return total_travel_time, average_travel_time
    
    except Exception as e:
        print("An error occurred while computing trip duration:", e)
        return None, None

def user_info(df):
    """
    Computes user information statistics.
    
    Args:
        df (DataFrame): Pandas DataFrame containing city data
        
    Returns:
        tuple: (user_type_counts, gender_counts, earliest_birth_year, recent_birth_year, common_birth_year)
    """
    try:
        # Compute counts of each user type
        user_type_counts = df['User Type'].value_counts()
        
        # Compute counts of each gender (if available)
        gender_counts = df['Gender'].value_counts() if 'Gender' in df.columns else None
        
        # Convert birth year column to numeric (if available)
        if 'Birth Year' in df.columns:
            df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce')
        
            # Compute earliest, most recent, and most common birth year
            earliest_birth_year = int(df['Birth Year'].min())
            recent_birth_year = int(df['Birth Year'].max())
            common_birth_year = int(df['Birth Year'].mode()[0])
        else:
            earliest_birth_year, recent_birth_year, common_birth_year = None, None, None
        
        return user_type_counts, gender_counts, earliest_birth_year, recent_birth_year, common_birth_year
    
    except Exception as e:
        print("An error occurred while computing user info:", e)
        return None, None, None, None, None

def display_statistics(df, city):
    """
    Displays statistics for the specified city.
    
    Args:
        df (DataFrame): Pandas DataFrame containing city data
        city (str): Name of the city being analyzed
    """
    # Define ANSI escape codes for color and bold text
    bold = '\033[1m'
    red_color = '\033[91m'
    green_color = '\033[92m'
    end_color = '\033[0m'  # Reset color to default
    
    print(f"\n{bold}{red_color}Statistics Computed{end_color}")
    print(f"\n{bold}{red_color}This is the information of {city}:{end_color}")

    # Compute and display popular times of travel
    common_month, common_day_of_week, common_hour_of_day = popular_times(df)
    print(f"\n{bold}{green_color}Popular Times of Travel:{end_color}")
    print("Most common month:", common_month)
    print("Most common day of week:", common_day_of_week)
    print("Most common hour of day:", common_hour_of_day)

    # Compute and display popular stations and trips
    common_start_station, common_end_station, common_trip = popular_stations(df)
    print(f"\n{bold}{green_color}Popular Stations and Trips:{end_color}")
    print("Most common start station:", common_start_station)
    print("Most common end station:", common_end_station)
    print("Most common trip from start to end:", common_trip)

    # Compute and display trip duration statistics
    total_travel_time, average_travel_time = trip_duration(df)
    print(f"\n{bold}{green_color}Trip Duration:{end_color}")
    print("Total travel time:", total_travel_time)
    print("Average travel time:", average_travel_time)

    # Compute and display user info
    user_type_counts, gender_counts, earliest_birth_year, recent_birth_year, common_birth_year = user_info(df)
    print(f"\n{bold}{green_color}User Info:{end_color}")
    print("Counts of each user type:")
    print(user_type_counts)
    if gender_counts is not None:
        print("Counts of each gender:")
        print(gender_counts)
    if earliest_birth_year is not None:
        print("Earliest birth year:", earliest_birth_year)
    if recent_birth_year is not None:
        print("Most recent birth year:", recent_birth_year)
    if common_birth_year is not None:
        print("Most common birth year:", common_birth_year)

def main():
    while True:
        # Get user input for city (chicago, new york city, washington)
        city = input("Enter city name (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            # Load data for the selected city
            df = load_data(city)

            # Display statistics for the selected city
            if df is not None:
                display_statistics(df, city)

            # Ask the user if they want to continue
            while True:
                choice = input("\nDo you want to Continue? (yes/no): ").lower()
                if choice == 'yes':
                    break
                elif choice == 'no':
                    print("Thank you for using the program. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")

            # If the user chooses to analyze another city, continue the loop
            # Otherwise, exit the program
            if choice == 'no':
                return
        else:
            print("Invalid city name. Please try again.")

if __name__ == "__main__":
    main()

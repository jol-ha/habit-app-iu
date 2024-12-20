import csv
import pandas as pd


# Helper functions

def dict_headers(csv_file_path):
    # Reads the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path) 
    # Takes the first row, excluding the date
    first_row = df.iloc[0, 1:]  # [1:] ignores the first column (e.g., 'date')
    # Converts the header and first row into a dictionary
    first_row_dict = first_row.to_dict()
    return first_row_dict

def remove_duplicates(csv_file_path):
    # Reads the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Drops rows with duplicate dates, keeping only the first occurrence
    df = df.drop_duplicates(subset=['date'], keep='first')
    
    # Returns the cleaned DataFrame
    return df

def select_daily_columns(cleaned_df, row_index=1):
    # Access the cleaned DataFrame
    df = cleaned_df
    
    # Filters columns that contain 'daily'
    daily_columns = df.columns[df.iloc[0].str.contains('daily', case=False, na=False)]
    
    # Returns the DataFrame with the filtered daily columns
    daily_df = df[daily_columns]
    return daily_df

def count_daily_results(daily_df):
    # Creates a dictionary to store counts of 'y', 'd', and 'n' for each column
    count_dict = {}
    
    # Iterates through each column and counts the standalone 'y', 'd', and 'n' values
    for column in daily_df.columns:
        # Initialize counts for 'y', 'd', and 'n'
        y_count = 0
        d_count = 0
        n_count = 0
        
        # Iterates through each value in the column
        for value in daily_df[column]:
            # Split each value into a list of words and check if 'y', 'd', or 'n' is in the list
            words = str(value).split()
            y_count += words.count('y')  # Count standalone 'y'
            d_count += words.count('d')  # Count standalone 'd'
            n_count += words.count('n')  # Count standalone 'n'
        
        # Calculate total count (y + d + n)
        total_count = y_count + d_count + n_count
        
        # To avoid division by zero, ensure total_count > 0 before calculating percentage
        if total_count > 0:
            percent_y = (y_count / total_count) * 100
        else:
            percent_y = 0  # Handle case where there are no 'y', 'd', or 'n' values
        
        # Store the counts and percentage in the dictionary
        count_dict[column] = {'y': y_count, 'd': d_count, 'n': n_count, 'percent_y': percent_y}
    
    # Return the result dictionary
    return count_dict

def max_daily_streak(series):
    streak = 0
    max_streak = 0
    for value in series:
        if value == 'y':
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return max_streak

def select_weekly_columns(cleaned_df, row_index=1):
    # Access the cleaned DataFrame
    df = cleaned_df
    
    # Filters columns that contain 'weekly'
    weekly_columns = df.columns[df.iloc[0].str.contains('weekly', case=False, na=False)]
    
    # Returns the DataFrame with the filtered weekly columns
    weekly_df = df[weekly_columns]
    return weekly_df

def max_weekly_streak(series):
    streak = 0
    max_streak = 0
    current_streak = 0

    # Iterates over the series in chunks of 7 days (weekly data)
    for i in range(0, len(series), 7):
        # Gets the 7-day window
        week = series[i:i+7]
        
        # Checks if there is at least one "y" in this week
        if 'y' in week.values:
            current_streak += 1
        else:
            # If no "y" in the 7 days, reset the streak
            max_streak = max(max_streak, current_streak)
            current_streak = 0

    # After the loop, ensures the last streak is considered
    max_streak = max(max_streak, current_streak)
    
    return max_streak

# Function to calculate weekly results
def count_weekly_results(weekly_df):
    # Counts the weeks (each week consists of 7 days)
    num_weeks = len(weekly_df) // 7
    
    # Initializes the result dictionary based on the columns of weekly_df
    results = {col: {"y": 0, "n": 0} for col in weekly_df.columns}
    
    # Counts "y" and "n" for each week
    for week in range(num_weeks):
        # Defines the week (7 days)
        week_data = weekly_df.iloc[week*7:(week+1)*7]
    
        for habit in results.keys():
            if "y" in week_data[habit].values:
                results[habit]["y"] += 1
            else:
                results[habit]["n"] += 1
    
    return results

# Main function for calculations

def calculations(csv_file_path):
    # Initial data processing
    first_row_data = dict_headers(csv_file_path)
    
    # Optional: Shows the raw DataFrame data
    df = pd.read_csv(csv_file_path) 
    print("\n\nCRUDE DATAFRAME\n")
    print(df.head())
    print(df.tail())
    
    # Remove duplicates
    cleaned_df = remove_duplicates(csv_file_path)
    
    # Optional: Shows the cleaned DataFrame
    print("\n\nDUPLICATES REMOVED\n")
    print(cleaned_df.head())
    print(cleaned_df.tail())
    
    # Select the daily columns
    daily_df = select_daily_columns(cleaned_df)
    
    # Shows the DataFrame with the daily columns
    print("\n\nDAILY DATAFRAME separated\n")
    print(daily_df.head())
    print(daily_df.tail())
    
    # Count 'y', 'd', and 'n' values
    result = count_daily_results(daily_df)
    
    # Shows the daily habit results
    print("\nDAILY HABIT RESULTS\n")
    for column, counts in result.items():
        print(f"Habit: {column:<25}, Yes_counts: {counts['y']:<3}, Percent y: {counts['percent_y']:>6.2f}%")
    
    # Calculate the daily streaks
    streaks = daily_df.apply(max_daily_streak)
    
    # Shows the maximum daily streaks
    print("\nDAILY STREAKS\nso many days you did the exercise continuously\n")
    print(streaks.to_string())
    
    # Select the weekly columns
    weekly_df = select_weekly_columns(cleaned_df)
    
    # Shows the DataFrame with the weekly columns
    print("\nWEEKLY DATAFRAME separated\n")
    print(weekly_df.head())
    print(weekly_df.tail())
    
    # Count the weekly results (Y/N for each week)
    weekly_results = count_weekly_results(weekly_df)
    
    # Shows the weekly habit results
    print("\n\nWEEKLY HABIT RESULTS\nperformance is only counted for entire weeks! \n")
    for habit, counts in weekly_results.items():
        total_weeks = counts["y"] + counts["n"]
        if total_weeks > 0:
            percentage_y = (counts["y"] / total_weeks) * 100
        else:
            percentage_y = 0
        print(f"for '{habit:<25}': yes_counts {counts['y']:<3}, percent_y = {percentage_y:.2f}%")
    
    # Calculate the maximum weekly streaks
    weekly_streaks = weekly_df.apply(max_weekly_streak)
    
    # Shows the maximum weekly streaks
    print("\nWEEKLY STREAKS\nso many weeks you did the exercise continuously\n")
    print(weekly_streaks.to_string())

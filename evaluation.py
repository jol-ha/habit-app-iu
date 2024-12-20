import csv
import pandas as pd

csv_file_path="test_data_file.csv"
def dict_header_row0(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path) 
    # Takes the first raw, without date
    first_row = df.iloc[0, 1:]  # [1:] ignoriert die erste Spalte (z.B. 'date')
    # converts header and row0 to a dictionary
    first_row_dict=first_row.to_dict()
    return first_row_dict

first_row_data = dict_header_row0(csv_file_path)

# optional Shows the raw data 
df = pd.read_csv(csv_file_path) 
print (df)

def remove_duplicates(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Drop rows with duplicate dates, keeping only the first occurrence
    df = df.drop_duplicates(subset=['date'], keep='first')
    
    # Return the updated DataFrame
    return df

# Call the function and store the result
cleaned_df = remove_duplicates(csv_file_path)

# optional Display the cleaned DataFrame
print("duplicates were removed\n")
print(cleaned_df.head())
print(cleaned_df.tail())

def select_daily_columns_by_row(cleaned_df, row_index=1):
    # Read the CSV file into a DataFrame
    df = cleaned_df
    
    # Access the specified row (e.g., row 1) and filter columns that contain 'daily'
    daily_columns = df.columns[df.iloc[0].str.contains('daily', case=False, na=False)]
    
    # Select the columns that match the filter from the DataFrame
    daily_df = df[daily_columns]
    
    # Return the filtered DataFrame
    return daily_df

# Call the function and store the result
daily_df = select_daily_columns_by_row(cleaned_df)

# Display the DataFrame with only the 'daily' columns based on the specific row
print(daily_df.head())
print(daily_df.tail())

def count_y_d_n(daily_df):
    # Lade die CSV-Datei in einen DataFrame
    df = daily_df
    
    # Erstelle ein Dictionary, um die Zählungen von 'y', 'd' und 'n' für jede Spalte zu speichern
    count_dict = {}
    
    # Gehe durch jede Spalte und zähle die 'y', 'd' und 'n' Werte
    for column in df.columns:
        y_count = df[column].str.contains('y', case=False, na=False).sum()  # Zähle 'y'
        d_count = df[column].str.contains('d', case=False, na=False).sum()  # Zähle 'd'
        n_count = df[column].str.contains('n', case=False, na=False).sum()  # Zähle 'n'
        total_count = y_count+d_count+n_count
        percent_y= y_count/total_count*100
        count_dict[column] = {'y': y_count, 'd': d_count, 'n': n_count, 'percent_y': percent_y}
    
    return count_dict



# Pfad zur CSV-Datei
csv_file_path = cleaned_df  # Ersetze dies mit deinem tatsächlichen Dateipfad

# Zähle die 'y', 'd' und 'n' Werte
result = count_y_d_n(daily_df)

# Gib die Zählungen für jede Spalte aus
for column, counts in result.items():
    print(f"Habit: {column:<25}, Yes_counts: {counts['y']:<3}, Percent y: {counts['percent_y']:>6.2f}%")

#Calculation of daily streaks
df = pd.DataFrame(daily_df)

# Function to calculate the maximal streak for each habit (column)
def max_streak(series):
    streak = 0
    max_streak = 0
    for value in series:
        if value == 'y':
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    return max_streak

# Calculate maximal streak for each habit
streaks = df.apply(max_streak)

# Print the results
print("STREAKS\n")
print(streaks.to_string())

def select_weekly_columns_by_row(cleaned_df, row_index=1):
    # Read the CSV file into a DataFrame
    df = cleaned_df
    
    # Access the specified row (e.g., row 1) and filter columns that contain 'daily'
    weekly_columns = df.columns[df.iloc[0].str.contains('weekly', case=False, na=False)]
    
    # Select the columns that match the filter from the DataFrame
    weekly_df = df[weekly_columns]
    
    # Return the filtered DataFrame
    return weekly_df

# Call the function and store the result
weekly_df = select_weekly_columns_by_row(cleaned_df)

# Display the DataFrame with only the 'daily' columns based on the specific row
print(weekly_df.head())
print(weekly_df.tail())

# Zähle die Anzahl der Wochen (jede Woche besteht aus 7 Tagen)
num_weeks = len(weekly_df) // 7

# Initialisiere das results Dictionary basierend auf den Spalten von weekly_df
results = {col: {"y": 0, "n": 0} for col in weekly_df.columns}

# Gehe durch jede Woche und zähle "y" und "n" für jede Spalte
for week in range(num_weeks):
    # Definiere die Wochenzeilen
    week_data = weekly_df.iloc[week*7:(week+1)*7]

    for habit in results.keys():
        # Wenn mindestens ein "y" in der Woche ist, setze die Woche auf "y"
        if "y" in week_data[habit].values:
            results[habit]["y"] += 1
        else:
            results[habit]["n"] += 1

# Ausgabe der Ergebnisse
for habit, counts in results.items():
    total_weeks = counts["y"] + counts["n"]
    if total_weeks > 0:
        percentage_y = (counts["y"] / total_weeks) * 100
    else:
        percentage_y = 0
    print(f"for '{habit:<25}': yes_counts {counts['y']:<3}, percent_y = {percentage_y:.2f}%")

df = weekly_df

# Function to calculate the maximal streak for each habit (column)
def max_weekly_streak(series):
    streak = 0
    max_streak = 0
    current_streak = 0

    # Iterate over the series in chunks of 7 days (weekly data)
    for i in range(0, len(series), 7):
        # Get the 7-day window
        week = series[i:i+7]
        
        # Check if there is at least one "y" in this week
        if 'y' in week.values:
            current_streak += 1
        else:
            # If no "y" in the 7 days, reset the streak
            max_streak = max(max_streak, current_streak)
            current_streak = 0

    # After the loop, ensure the last streak is considered
    max_streak = max(max_streak, current_streak)
    
    return max_streak

# Calculate maximal streak for each habit (column)
weekly_streaks = df.apply(max_weekly_streak)

# Print the results
print("STREAKS\n")
print(weekly_streaks.to_string())



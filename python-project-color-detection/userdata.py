import pandas as pd
import os
import time
import subprocess

def read_user_data():
    try:
        # Read the user data from the CSV file
        df = pd.read_csv('user_data.csv')
        return df
    except Exception as e:
        print(f"Error reading user data from CSV file: {e}")
        return None

def write_user_data(df):
    try:
        # Write the DataFrame to a CSV file
        df.to_csv('user_data.csv', index=False)
        print("User data has been saved to user_data.csv")
    except Exception as e:
        print(f"Error writing user data to CSV file: {e}")

def get_user_id(user_name):
    # Read the user data
    df = read_user_data()
    
    if df is not None:
        # Check if the user already exists in the DataFrame
        if user_name in df['User'].values:
            # Get the user's ID
            user_id = df.loc[df['User'] == user_name, 'ID'].values[0]
            return user_id
        else:
            # Generate a new user ID
            if len(df) == 0:
                user_id = 1
            else:
                user_id = df['ID'].max() + 1
            
            # Add the user to the DataFrame
            new_user = pd.DataFrame({'ID': [user_id], 'User': [user_name], 'Color': [''], 'Image': ['']})
            df = pd.concat([df, new_user], ignore_index=True)
            
            # Write the updated DataFrame to the CSV file
            write_user_data(df)
            
            return user_id

def update_user_data(user_id, user_name=None, user_color=None, user_image=None):
    # Read the user data
    df = read_user_data()
    
    if df is not None:
        # Check if the user already exists in the DataFrame
        if user_id in df['ID'].values:
            # Check if the user has changed their name
            if user_name is not None and user_name != df.loc[df['ID'] == user_id, 'User'].values[0]:
                print(f"Welcome back, {user_name}! Your name has been updated.")
            
            # Update the user's color and image
            if user_color is not None:
                df.loc[df['ID'] == user_id, 'Color'] = user_color
            if user_image is not None:
                df.loc[df['ID'] == user_id, 'Image'] = user_image
        else:
            # Add the user to the DataFrame
            new_user = pd.DataFrame({'ID': [user_id], 'User': [user_name], 'Color': [user_color], 'Image': [user_image]})
            df = pd.concat([df, new_user], ignore_index=True)
            print(f"Welcome, {user_name}!")
        
        # Write the updated DataFrame to the CSV file
        write_user_data(df)
# Define user_id variable
# Define user_id variable
    user_id = None

def main():

    print("Welcome to my program!")

# Get the user's name
user_name = input("What is your name? ")

while True:
    # Ask the user what they want to do
    print(f"\nHello {user_name}! What would you like to do?")
    print("1. Check if a file exists")
    print("2. Open a text file")
    print("3. Open colorscanner.py")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        # Check if a file exists
        file_path = input("Please enter the path to the file: ")
        if os.path.exists(file_path):
            print("File exists!")
        else:
            print("File does not exist.")

    elif choice == '2':
        # Open a text file
        file_path = input("Please enter the path to your text file: ")
        if os.path.exists(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                contents = f.read()
                print(contents)
        else:
            print("Invalid file path or file type. Please enter a valid path to a text file.")
    
    elif choice == '3':
        # Open colorscanner.py
        file_path = r"C:\Users\workplace\Documents\GitHub\Ai_project\python-project-color-detection\colorscanner.py"
        if os.path.exists(file_path) and file_path.endswith('.py'):
            print("Running colorscanner.py...")
            time.sleep(2) # Add a delay for the loading message
            os.system(f"python {file_path}")
        else:
            print("Invalid file path or file type. Please enter a valid path to a Python file.")
    
    elif choice == '4':
        # Exit the program
        print("Goodbye!")
        break

    else:
        # Invalid choice
        print("Invalid choice. Please enter a number between 1 and 4.")
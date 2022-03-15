import os
import re
import stat
from datetime import datetime

description = {0: "File type and permissions", # Dictionary with window's os.stat descriptions
               1: "File index on Windows",
               2: "Device identifier",
               3: "Number of hard links",
               4: "User identifier of file owner(linux)",  # Useless on Windows
               5: "Group identifier of file owner(linux)",  # Useless on Windows
               6: "Size of file in bytes",
               7: "Date of last file access",
               8: "Date of most recent modification",
               9: "Creation date"}


def adjust_dictionary(dictionary): # Function that changes dictionary descriptions to reflect linux os.stat info
    dictionary[1] = "Inode number"
    dictionary[4] = "User identifier of file owner"
    dictionary[5] = "Group identifier of file owner"
    dictionary[9] = "Date of most recent metadata change"


def get_metadata(x, data): # Function that gets and returns metadata and returns string with appropriate description
    if os.name == "nt":  # Checks if windows system
        if x == 4 or x == 5:  # Descriptions 4 & 5 are only for linux systems, passes items.
            pass
        elif x >= 7: # Returns string with description item and formatted related metadata
            return f"{description[x]} : {datetime.fromtimestamp(data[x])}"
        else:
            return f"{description[x]} : {data[x]}" # Returns string with description item and the related metadata
    else: # Else statement to return strings with linux descriptions and the related metadata
        if x == 0:
            adjust_dictionary(description) # Calls function to change dictionary values to reflect linux os.stat info
            return f"{description[x]} : {stat.filemode(data[x])}" # Converts permissions value to reflect linux format
        elif x >= 7: # Returns string with description: metadata with converted date time to a readable format
            return f"{description[x]} : {datetime.fromtimestamp(data[x])}"
        else:
            return f"{description[x]} : {data[x]}" # Returns string with description item and the related metadata


def name_file(file_path): # Function for allowing the user to name the file that saves the metadata of the file or dir
    auto_name = os.path.basename(file_path) # If user doesn't enter name uses dir/file basename as name for file
    name_check = re.compile(r"""[="+'@!#$%^&*()`<>?/|{}~:\\ ]""") # regex that compiles illegal filename characters
    while True: # while loop that runs until user enters a file name with legal filename characters
        name = input("What would you like to name the file?: ") # ask user for desired filename
        if name_check.search(name) is None: # regex that checks for illegal filename characters
            if name == "": # if the user leaves the name blank, returns the autoname variable
                return auto_name
            else:
                return name # returns user entered name
        else: # lets the user know that they entered an invalid file name
            print(r"""The file name contains illegal characters: ='"@!#$%^&*()<>?/\|{}~:`+ """)


def txt_metadata_file(path):  # Function that gets and saves metadata of the file they entered to a text file
    file_metadata = os.stat(path)  # Gets metadata for the file and stores in variable
    file_name = name_file(path) # Calls the file naming function
    with open(f"{file_name}_metadata.txt", "w") as file:  # Opens file to write metadata to
        file.write(f"File Name: {os.path.basename(path)}\n")  # Writes path file name for user
        for x in range(10):  # for loop that runs through numbers 0-9
            data = get_metadata(x, file_metadata) # variable that stores get_function
            if data is not None: # returns the respective metadata for item in loop if the item has metadata
                file.write(f"{data}\n") # writes the metadata to a line in the saved file
            else: # else statement to pass items in the for loop that don't have metadata (ie item 4 or 5 for windows)
                pass
    print(f"The metadata has been saved to {file_name}_metadata.txt\n") # indicates data has been saved and name of file


def print_metadata_file(path):  # Gets and prints metadata of a file to the screen
    file_metadata = os.stat(path)
    print(f"\nFile Name: {os.path.basename(path)}") # prints name of file to screen for suer reference
    for x in range(10):
        data = get_metadata(x, file_metadata)
        if data is not None:
            print(data) # prints metadata of the file to the screen
        else:
            pass
    print() # blank print statement to indicate to user program has finished getting metadata for that file


def txt_metadata_dir(path):  # Gets and saves the metadata of all the files in a directory to a file
    dir_data = os.scandir(path)  # Scans the directory for all the files and stores in variable
    file_name = name_file(path)  # Calls the name_file stores in variable
    with open(f"{file_name}_metadata.txt", "w") as file:  # Opens file to write metadata to using the user inputted name
        for item in dir_data:  # For loop to run through the directory and write the metadata of each file
            if os.path.isfile(item): # if statement that determines if the current item is a file vs another directory
                file.write("------------------------------------\n") # Code to make the written output easier to read
                file.write(f"File Name: {item.name}\n")
                file.write("------------------------------------\n")
                get_data = os.stat(item)
                for x in range(10):
                    data = get_metadata(x, get_data)
                    if data is not None:
                        file.write(f"{data}\n")
                    else:
                        pass
    print(f"The metadata has been saved to {file_name}_metadata.txt\n")  # Lets user know the metadata was saved


def print_metadata_dir(path):  # Prints the metadata of all the files in a directory to screen
    dir_data = os.scandir(path)
    for item in dir_data:
        if os.path.isfile(item):
            print("------------------------------------")
            print(f"File Name: {item.name}")
            print("------------------------------------")
            get_data = os.stat(item)
            for x in range(10):
                data = get_metadata(x, get_data)
                if data is not None:
                    print(data)
                else:
                    pass
    print()

try: # try block with main program while loop
    while True:
        user_path = input("Enter a File or Directory Path(Type Quit to exit): ") # asks user for file or dir path
        if os.path.exists(user_path): # checks if path exists, if not returns to asking user for file or dir path
            while True: # while loop that runs until user enters valid input
                user_choice = input("Would you like to save the metadata to a file?(Type 'Y' or 'N'): ").lower()
                if os.path.isfile(user_path):
                    if user_choice == "y":
                        txt_metadata_file(user_path)
                        break                          # if statements that determine whether the user entered file path
                    elif user_choice == "n":           # or directory path and whether they want to save or print and
                        print_metadata_file(user_path) # calls the appropriate get metadata function
                        break
                if os.path.isdir(user_path):
                    if user_choice == "y":
                        txt_metadata_dir(user_path)
                        break
                    elif user_choice == "n":
                        print_metadata_dir(user_path)
                        break
        elif user_path == "quit": # allows user to exit the program by entering "quit"
            print("User exited.")
            break
        else:
            print("Please enter a valid path.") # else statement that lets user know the path they entered is invalid
except KeyboardInterrupt: # exception block for keyboard interrupts, exits out of program
    print("\nUser exited.")



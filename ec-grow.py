#!/usr/bin/env python3                             
from datetime import datetime
import pandas as pd
import os, re, argparse

parser = argparse.ArgumentParser()                 # To take arguments from cli
parser.add_argument("files", nargs="+")            # Adds the argument files
opts = parser.parse_args()

print("Created by Bevan Stanely aka chain-ed-reaction for BEE LAB")

####### Get Time

def get_datetime():                                # A function to get the current date and time
    now = datetime.now()                           # Pulls the current date and time
    dt_string = now.strftime("%d_%m_%Y_%H_%M")     # Trims now too get dd_mm_YY_HH_MM format
    return dt_string                               # Returns the current date and time as a string
now = str(get_datetime())                          # Calls the get_datetime function and assigns the returned value to a 
                                                   # variable
                                                   
####### Get Time ########

output = "result-" + now + ".csv"                  # Assign the name for output file as a string with unique name
tempfile = open( str("temp-" + now + ".csv"), "a+")# Assign the name for temp file as a string with unique name and open 
file_order = 0                                     # A variable to normalise the iteration number when dealing with
                                                   # multiple files
LastIteration = [0]                                # Same as above but local

####### Write Header

cell_num = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']
                                                   # A list of all headers with location for 96 well plates
pattern = "\t"                                     # Assigns a delimiter
pattern = pattern.join(cell_num)                   # Joins the header list with the delimiter specified
tempfile.write("Iteration\t" + pattern + "\n")     # Writes the header to a tempfile

####### Write Header #######


####### Merge Results 

for file in opts.files:                            # A loop which goes throught all the files in the commandline call
    with open( file , 'r') as f:                   # Opens the file parameter in the function as readable
        lines = f.readlines()                          # A list of all the lines in the file
        for i, line in enumerate(lines):               # A loop function that will iterate over each line of the file
            if line.startswith('\tIteration'):     # An if condition to select a iteration
                temp = re.search(r'\d+', str(line.strip())).group() # Gets the iteration number
                temp = int(temp, base = 10)        # Convert iteration number into an integer
                Iteration = [0]                    # Declares a list with 0 as sole element
                Iteration[0] = (temp)              # Assigns the iteration value to the the index 0
                Iteration[0] = Iteration[0] + file_order # Adds the file order which specifies the current number of files
                LastIteration[0] = Iteration[0]    # Assigns the current iteration as last iteration
                Iteration[0] = str(Iteration[0])   # Converts the integer into a string
                row1 = lines[i + 1].splitlines()   # Selects all 8 rows ahead and splits the individual elements into strings
                row2 = lines[i + 2].splitlines()
                row3 = lines[i + 3].splitlines()
                row4 = lines[i + 4].splitlines()
                row5 = lines[i + 5].splitlines()
                row6 = lines[i + 6].splitlines()
                row7 = lines[i + 7].splitlines()
                row8 = lines[i + 8].splitlines()
                Onetime = Iteration + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 # Merges all the lists
                s = ""                             # No delemiter hence empty string
                s = s.join(Onetime)                # Joins the list into a string
                tempfile.write(s + "\n")           # Writes the line to the current line and specifies new line in the end
        f.close()                                  # The file is closed
    file_order = LastIteration[0]                  # Sets the highest iteration value as an int
tempfile.close()                               # Close the tempfile

####### Merge Results #######


tempfile1 = str("temp-" + now + ".csv")        # Declares the tempfile created previously
with open( tempfile1 , 'r') as f:              # Opens the tempfile in reading mode
    results_df = pd.read_csv(f, delimiter = '\t')    # A dataframe is assigned
    t0_results_df = results_df.iloc[[0]].values[0]   # The t0 values are selected
    normalized_values = results_df.sub(t0_results_df)# The t0 values are subtracted from all other timepoint values
    normalized_values.index.name = 'time_point'# Sets a new name to the index column
    normalized_values.drop("Iteration", axis=1, inplace=True) # Deletes the iteration column and sets the value to the original dataframe
    normalized_values.to_csv(output)           # The normalised values are saved onto an outputfile
    f.close()                                  # Close the tempfile
os.remove("temp-" + now + ".csv")              # Delete the tempfile
print("The normalised file is saved as " + output + " in the current directory")
print("Done")                                  # Marks the end of the program

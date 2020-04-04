#!/usr/bin/env python3                             
from datetime import datetime                      # Need to install exrex, pandas
import pandas as pd                                # A library to work with dataframes
import os, sys, re, argparse, exrex, csv
parser = argparse.ArgumentParser()                 # To take arguments from cli
parser.add_argument("files", nargs="+")            # Adds the argument files
opts = parser.parse_args()
def get_datetime():                                # A function to get the current date and time
    now = datetime.now()                           # Pulls the current date and time
    dt_string = now.strftime("%d_%m_%Y_%H_%M")     # Trims now too get dd_mm_YY_HH_MM format
    return dt_string                               # Returns the current date and time as a string
now = get_datetime()                               # Calls the get_datetime function and assigns the returned value to a 
                                                   # variable
output = "result-" + now + ".csv"                  # Assign the name for output file as a string with unique name
tempfile = open( "temp-" + now + ".csv", "a+")     # Assign the name for temp file as a string with unique name and open 
file_order = 0                                     # A variable to normalise the iteration number when dealing with
                                                   # multiple files
LastIteration = [0]                                # Same as above but local
def write_header():                                # Generates a header line and writes it to temp file
    #cell_num = [ 'Iteration' ] +  (list(exrex.generate('[A-H][1-9]|[A-H][1][0-2]')))
    cell_num = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D11', 'D12', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E11', 'E12', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H11', 'H12']
    pattern = "\t"
    pattern = pattern.join(cell_num)
    tempfile.write("Iteration\t" + pattern + "\n")
    print("Iteration\t" + pattern + "\n")
def extract_n_write_OD_values(f):
    lines = f.readlines()
    for i, line in enumerate(lines):
            if line.startswith('\tIteration'):
                temp = re.search(r'\d+', str(line.strip())).group()
                temp = int(temp, base = 10)
                Iteration = [0]
                Iteration[0] = (temp)
                Iteration[0] = Iteration[0] + file_order
                LastIteration[0] = Iteration[0]
                Iteration[0] = str(Iteration[0])
                row1 = lines[i + 1].splitlines()
                row2 = lines[i + 2].splitlines()
                row3 = lines[i + 3].splitlines()
                row4 = lines[i + 4].splitlines()
                row5 = lines[i + 5].splitlines()
                row6 = lines[i + 6].splitlines()
                row7 = lines[i + 7].splitlines()
                row8 = lines[i + 8].splitlines()
                Onetime = Iteration + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8
                s = ""
                s = s.join(Onetime)
                tempfile.write(s + "\n")
def reorganise_data(ftbc):
    global file_order, LastIteration
    with open( ftbc , 'r') as f:
        extract_n_write_OD_values(f)
        f.close()
    file_order = LastIteration[0]
def merge_results():
    for file in opts.files:
        reorganise_data(file)
    tempfile.close()
def normalize_values():    
    with open( 'tempfile.csv' , 'r') as f:
        results_df = pd.read_csv(f, delimiter = '\t' )
        t0_results_df = results_df.iloc[[0]].values[0]
        normalized_values = results_df.sub(t0_results_df)
        normalized_values.to_csv(output)
    tempfile.close()
    os.remove("temp-" + now + ".csv")
write_header()
merge_results()
normalize_values()
print("Done")
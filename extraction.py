#!/usr/bin/env python3

"""Module that allows cleaning accoustic parameters extracted from Audacity (with Aurora 
acoustical parameters module) currently it works only for an specific output format from 
Audacity (it doesn't suppor Audition+Aurora)

How to call this function?: From the console, write:
$ python3 cleaner.py aurora_output_file.csv classname_of_that_file

For more info on what's the format of the input file, look 'auroraANDaudacity_outputs' and
'Documentation' folders

Details that are recommended to improve in the future:

1. In the function 'calculateParameters' manage the output parameters_chanels.append('No Result!!')
to append some VALID VALUE i.e. -> A valid number for that parameter (either a calculation or an aproximation
of the real value)

2. In the function 'calculateParameters', the management of null or not valid values can be improved

3. Add support for directories (clean a whole directory and not only FILE by FILE)"""

import pandas as pd
from sys import argv
import csv

# Validate that the file and classname (classification) were passed in the args
try:
    filename = argv[1]
    classification = argv[2]   
except:
    raise Exception('File not found, be sure to enter a valid filename (csv format)'
                     + ' and a valid classification (of sound)')

def getcol_from_table(column, table):
    """Code that get the name of an specific column in the table, it can handle either an specific column or a list of columns
    'column' specifies the column you want to pick from the table, 
    'table' specifies the target table (where you want to pick that column)"""
    
    if isinstance(column, int):  # Get only 1 column (then input must be an integer)
        return 'col_'+str(column+(15* (table-1)))  # For more info about this formula, see "Documentation/cleaningRules.md"
    elif isinstance(column, list):  # Get several columns (then input must be a list)
        cols = ['col_'+str(column[i]+(15* (table-1))) for i in range(len(column))]
        return tuple(cols)

# Determines if a string can be converted to number
def is_number(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False

def calculate_parameters(df, columns, displacement):
    """Get values from each parameter and return a tuple with the average of each parameter
    df: dataframe, columns: each selected column, displacement: It can be either 0 (left chanel) or 29 (right chanel)
    For info about the parameters extraction read Documentos/reglasDeLimpieza.md """
    
    parameters_chanels = []  # Either left or right chanel
    for row in (5+displacement, 6+displacement, 7+displacement, 14+displacement):
        parameter = []
        for col in columns:
            value = df[col][row]
            print(col, row)
            if isinstance(value, str):
                value = value.replace(',','.')
                if is_number(value):
                    parameter.append(float(value))
        # Calculate the average of the parameter
        if len(parameter) != 0:
            average = sum(parameter) / len(parameter)
            # Add the average of each parameter to the list of parameters (senial, ganancia, etc)
            parameters_chanels.append(average)
        else: # No entry was a number, a label is added to 'parameters_chanels'
            # This case happens oftenly when there's only one sound channel (i.e. LEFT CHANNEL)
            # And the cleaner script try to visit the RIGHT CHANNEL positions (which are null)
            parameters_chanels.append('No Result!!')
    return tuple(parameters_chanels)

def cleanfile_writeoutput(df, output_filename):  # df == dataframe
    """clean a csv file and write its output in csv format"""

    i = 1  # Index for handling the 'current_table'
    left_tables = len(df.columns) // 15 + 1
    with open(output_filename+'_salida.csv', mode='w') as output_file:
        csv_writer = csv.writer(output_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write header
        csv_writer.writerow(['Signal, Noise, StrengTH, T20, Signal_r, Noise_r, StrengTH_r, T20_r, Classification'])
        while (left_tables > 0):
            left_tables -= 1
            columns = getcol_from_table([6,7,8,9,10], i)  # Get cols from 6 to 10

            pciz = calculate_parameters(df, columns, 0) # Left chanel parameters
            pcdc = calculate_parameters(df, columns, 29) # Right chanel parameters

            # Write parameters (from both chanels) in the output file (.csv)
            csv_writer.writerow([pciz[0],pciz[1],pciz[2],pciz[3],pcdc[0],pcdc[1],pcdc[2],pcdc[3],classification])
            i += 1

def read_file(filename):
    """ Read '.csv' and return pandas dataframe with its content"""
    # Validate file extension, open file and start cleaning
    if  filename.endswith('.csv') and len(filename)>4:
        dataframe = pd.read_csv(filename, encoding='utf-8', nrows=60)
    else:
        raise Exception('File couldn\'t be read, be sure to enter a valid filename with "csv" extension')

    # Name columns of dataframe (col_0, col_1, ..., col_n)
    column_names = list('col_'+str(i+1) for i in range(len(dataframe.columns)))
    dataframe.columns = column_names
    return dataframe

if __name__ == '__main__':
    dataframe = read_file(filename)

    delimiter = ''
    while (len(delimiter) != 1):
        delimiter = input("Please enter the delimiter you want to use as separator.\nExample: '.' OR ';' OR ',' ETC\n")

    print('cleaning file: ', filename)
    cleanfile_writeoutput(dataframe, filename.rsplit('.')[0])
    print('Done!\n')
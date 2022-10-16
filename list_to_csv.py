import pandas as pd # Importing Python's Pandas library
import os
import csv

python_list = [1, 2, 3, 4, 5, "Test", "Test2"] # A Python list filled with integers and strings
test_df = pd.DataFrame(python_list) # Creating a Pandas Dataframe made of our "python_list"
test_df.to_csv('result.csv', index = False, header = False) # Saving the Dataframe containing our "python_list" as a CSV file named "result.csv"
print("Done")
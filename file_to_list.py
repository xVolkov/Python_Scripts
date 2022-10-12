'''
    This script transforms a text file's contents to a Python list
'''

File = open('file.txt', 'r') # Python handler to open your .txt file to read its data
contents = File.read() # Reads your .txt file's data
lines = contents.split('\n') # Creates a Python list made up of each line in your .txt file (line 1 = item 1, line 2 = item 2, etc...)
for line in lines: # Prints each item in your python list (item by item == line by line)
    print(line) # Prints list contents item-by-item
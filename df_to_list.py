# Extracts 'column_name1' column from the dataframe (our dataframe variable is 'df')
data = df['column_name1'].copy()
data.dropna() # drops duplicates

# Converts Pandas dataframe to a python list
data_listed = data.tolist() # we created a new list and appended 'ips' to it as a list
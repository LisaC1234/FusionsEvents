
# Import pandas package  
import pandas as pd 
  
# Define a dictionary containing Students data 
data = {'Name': ['Princi', 'Princi', 'Gaurav', 'Anuj'], 
        'Height': [5.1, 6.2, 5.1, 5.2], 
        'Qualification': ['Msc', 'MA', 'Msc', 'Msc']} 
  
# Define a dictionary with key values of 
# an existing column and their respective 
# value pairs as the # values for our new column. 
dico = {'Princi' : '1', 'Gaurav':'2', 'Anuj':'3'}

# Convert the dictionary into DataFrame 
df = pd.DataFrame(data) 
print(df)
# Provide 'Address' as the column name 
df['Address'] = [dico[x] for x in df['Name']]
  
# Observe the output 
print(df) 


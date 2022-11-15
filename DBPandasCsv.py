import pyodbc
import csv
import pandas as pd


#### DATABASE CREDENTIALS ####
server = 'SERVERNAME'
database = 'DATABASENAME'
username = 'USER'
password = 'PASSWORD'
conn = pyodbc.connect('DRIVER={DRIVER NAME WITH BRACKETS INCLUDED};SERVER='+server+';\
     DATABASE='+database+';UID='+username+';PWD='+ password)
conn_str = 'DRIVER={DRIVER NAME WITH BRACKETS INCLUDED};SERVER='+server+';\
		      DATABASE='+database+';UID='+username+';PWD='+ password
cursor = conn.cursor()



#### CREATE A FUNCTION THAT FETCHES DATA USING AN SQL QUERY AND RETURNS IT IN A PYTHON LIST ####
def run_sql(sql) -> list:
	sql = sql
	with pyodbc.connect(conn_str) as conn:
		cursor = conn.cursor()
		conn.autocommit = True
		cursor.execute(sql)
		return [list(row) for row in cursor.fetchall()]
		cursor.close()
		del cursor
    
    
#### WRITE YOUR SQL ####
sql = ''' WRITE YOUR SQL HERE '''


#### USE THE FUNCTION TO PUT YOUR QUERY DATA INTO A LIST ####

data = run_sql(sql)

#### IF YOU WANT IT IN A PANDAS DATAFRAME DO THIS ####

#### Write the list of lists into a CSV file 
write_file = '~/directory/filename.csv'
with open(write_file,'w') as f:
    writer = csv.writer(f, delimiter = ',', lineterminator='\n')
    writer.writerows(data)

		      
#### Create a list of column names based on your data source
names = ['column 1','column2','column3',...]		      
		      
#### Read the file into a DataFrame
df = pd.read_csv(write_file, names = names, usecols=names)
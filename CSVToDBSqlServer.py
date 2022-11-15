import pyodbc
from azure.storage.blob import BlockBlobService

#### These are your Azure Blob storage credentials ####
AZB_CREDS = {
	'STORAGEACCOUNTNAME': "ACCOUNT NAME",
	'STORAGEKEY': "###################",
	'CREDENTIAL': 'AzureStorageCredential',
	'FILEFORMAT': 'generic_csv_format', # 
}


#### This function creates an external data source on your database that points to blob storage ####
def asdb_create_external_data_source(table_name, container_name) -> None:
	q_extds = '''
	CREATE EXTERNAL DATA SOURCE {table_name}_asdb_storage 
	WITH
	(
	    TYPE = BLOB_STORAGE, 
	    LOCATION='https://{blob_address_here}/{container_name}'
	)
	'''.format(table_name=table_name,container_name=container_name)
	# LOCATION ='wasbs://{container_name}@{storage_account_name}.blob.core.windows.net',
	with pyodbc.connect(conn_str) as conn:
		cursor = conn.cursor()
		conn.autocommit = True
		try:
			cursor.execute(q_extds)
			print('External data source created for the following container: {}'.format(container_name))
		except Exception as e:
			# print 'Error with creating external data source for the following container: {} \nHere is the error: {}'.format(container_name,e)
			pass
		cursor.close()
		del cursor
		conn.autocommit = False


#### This function drops a temporary version of a table with the string _tmp at the end ####
def drop_temp_table(schema, table) -> None:
	sql = '''
	DROP TABLE {schema}.{table}_tmp;
	'''.format(table=table, schema=schema)
	with pyodbc.connect(conn_str) as conn:
		cursor = conn.cursor()
		conn.autocommit = True
		try:
			cursor.execute(sql)
			print('Table {schema}.{table}_tmp dropped.'.format(schema=schema,table=table))
		except Exception as e:
			# print 'Error dropping external table dbo.{}\nError: {}'.format(table_name,e) # errors when the table doesn't exist - all good
			pass
		cursor.close()
		del cursor
		conn.autocommit = False


#### This function creates a temporary table from the target table you want to push data to ####
def create_temp_table(schema,table_name) -> None:
	with pyodbc.connect(conn_str) as conn:
		cursor = conn.cursor()
		conn.autocommit = True
		sql = '''
		select *
		into {schema}.{table_name}_tmp
		from {schema}.{table_name}
		where 1 = 0;
		'''.format(schema=schema,table_name=table_name)
		# print sql
		cursor.execute(sql)
		print('Created temp table [{}].[{}]'.format(schema,table_name+'_tmp'))
		cursor.close()
		del cursor
		conn.autocommit = False
  
#### This function inserts a csv file from blob storage into the target table ####
def bulk_insert(schema, table_name, data_source_name, container_file_name, field_terminator=',', row_terminator='0x0a') -> str:
    sql = '''
    BULK INSERT {schema}.{table_name}
    FROM '{container_file_name}'
    WITH (DATA_SOURCE = '{data_source_name}',ROWTERMINATOR='{row_terminator}',FIELDTERMINATOR='{field_terminator}', FORMAT='CSV', CODEPAGE = '65001')
    '''.format(schema=schema,table_name=table_name
      ,container_file_name=container_file_name,data_source_name=data_source_name
      ,field_terminator=field_terminator,row_terminator=row_terminator)
    # print(sql)
    with pyodbc.connect(conn_str) as conn:
      cursor = conn.cursor()
      conn.autocommit = True
      message = 'Success'
      try:
        cursor.execute(sql)
      except Exception as e:
        print('Error with bulk insert: {} \nHere is the error: {}'.format(container_file_name,e))
        message = 'Error with bulk insert: {} \nHere is the error: {}'.format(container_file_name,e)

    cursor.close()
    del cursor
    conn.autocommit = False	
    return message
  
  
  
#### This function merges the temporary table with the main table using a list of unique keys ####
def merge_temp_table_with_main(schema,table_name,list_of_unique_fields):
  tbl = '{schema}.{table_name}'.format(schema=schema,table_name=table_name)
  tmp_tbl = tbl+'_tmp'
  unique_where_filter_string = 'AND '.join(['coalesce({tbl}.{col},\'NULL\') = coalesce({tmp_tbl}.{col},\'NULL\')\n'.format(col=c,tbl=tbl,tmp_tbl=tmp_tbl) for c in list_of_unique_fields])
  sql = '''
  delete from {schema}.{table_name} 
  where exists (select 1 from {schema}.{table_name}_tmp where {unique_where_filter_string});
  insert into {schema}.{table_name} select * from {schema}.{table_name}_tmp;
  drop table {schema}.{table_name}_tmp;
  '''.format(schema=schema,table_name=table_name
    ,unique_where_filter_string=unique_where_filter_string)
  #print sql
  with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    conn.autocommit = True
    try:
      cursor.execute(sql)
      print('Successful merge into {}.{}.'.format(schema,table_name))
      message = 'Successful merge into {}.{}.'.format(schema,table_name)
    except Exception as e:
      print('Error with the merge into {}.{}\nError: {}'.format(schema,table_name,e))
      # pass
      message = 'Error with the merge into {}.{}\nError: {}'.format(schema,table_name,e)
    cursor.close()
    del cursor
    conn.autocommit = False
  return message

  
write_file = '~/directory/file.csv'

### STEP 1: Create a new blob in your container of choice in azure blob storage using your csv file. This function uses the create_blob_from_path function from the azure blob api
container_name = 'NAME OF YOUR CONTAINER'
container_file_name = 'file.csv'.format(today)
blob_service = BlockBlobService(account_name=AZB_CREDS['STORAGEACCOUNTNAME'], account_key=AZB_CREDS['STORAGEKEY'])

blob_service.create_blob_from_path(container_name, container_file_name, write_file) # this always overwrites whatever is in the container
print('Done sending txt file up to AZB ...')

### STEP 2: Create an external data source that ties a specified database table to a container in blob storage
target_schema = 'schema'
table_name = 'table'
data_source_name = table_name+'_asdb_storage' # you can create this on the next line 
asdb_create_external_data_source(table_name, container_name) 

### STEP 3: If a temporary table already exists, drop it. Then create a new temporary table to push the CSV file to
drop_temp_table(target_schema, table_name)
create_temp_table(target_schema, table_name)

### STEP 4: Insert the CSV file from blob storage into the temporary table
bulk_insert(target_schema,table_name+'_tmp', data_source_name, container_file_name)

### STEP 5: Merge the CSV data into the existing table using merge criteria from the temporary table
unique_columns = ['column1','column2','column3',[n].....]
merge_temp_table_with_main(target_schema,table_name,unique_columns)
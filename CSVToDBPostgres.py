import psycopg2

HOST = 'HOSTNAME'
DB = 'DBNAME'
USER = 'USERNAME'
PASSWORD = 'PASSWORD'
PORT = 'PORT'
 
conn = psycopg2.connect(host=HOST,database=DB,user=USER,password=PASSWORD,port=PORT)
 
# cursor = conn.cursor()
 
# this can bulk insert a file into a table
def copy_file_into(schema, table, file, delimiter=',',null='NULL',columns=[]):
    cursor = conn.cursor()
    fpath = open(file,'r')
    if len(columns) > 0:
        cols_str = ','.join(columns)
        copy_sql = f'''COPY {schema}.{table} ({cols_str}) FROM STDIN WITH CSV DELIMITER E'{delimiter}' QUOTE '"' NULL '{null}';''' # allows there to be embedded commas which in NICE!!
    else:
        copy_sql = f'''COPY {schema}.{table} FROM STDIN WITH CSV DELIMITER E'{delimiter}' QUOTE '"' NULL '{null}';''' # allows there to be embedded commas which in NICE!!
    # copy_sql = f'''COPY {schema}.{table} FROM STDIN WITH CSV DELIMITER E'\t' QUOTE '"' NULL 'NULL';''' # allows there to be embedded commas which in NICE!!
    print(copy_sql)
    cursor.copy_expert(copy_sql, fpath)
    print('Done with the copy')
    cursor.execute('COMMIT;')
    cursor.close()
    del cursor
 
# use this to merge data from one table to another - you just need to define the sources, targets and primary key fields
def merge_one_table_with_main(source_schema,target_schema,source_table,target_table,list_of_unique_fields):
    # unique_where_filter_string = 'AND '.join(['{target_schema}.{target_table}.{col} = {source_schema}.{source_table}.{col}\n'.format(col=c,target_table=target_table,source_table=source_table,source_schema=source_schema,target_schema=target_schema) for c in list_of_unique_fields])
    unique_where_filter_string = 'AND '.join([f'{target_schema}.{target_table}.{col} = {source_schema}.{source_table}.{col}\n' for col in list_of_unique_fields])
    sql = f'''
    delete from {target_schema}.{target_table}
    where exists (select 1 from {source_schema}.{source_table} where {unique_where_filter_string});
    insert into {target_schema}.{target_table} select * from {source_schema}.{source_table};
    drop table {source_schema}.{source_table};
    COMMIT;'''   
    # print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    del cursor


def create_temp_table(schema, table, temp_table):
   sql = f'''
   DROP TABLE IF EXISTS {schema}.{temp_table};
   SELECT * INTO {schema}.{temp_table} FROM {schema}.{table} WHERE 1 = 0;
   COMMIT;
   '''
   cursor = conn.cursor()
   cursor.execute(sql)
   cursor.close()
   del cursor
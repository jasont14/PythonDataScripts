import pandas as pd

path = 'path/todata/csv'
data=pd.read_csv(path)
        

#### Drop Columns
def drop_columns(self, col_list):
    if len(col_list)>0:    
        data=data.drop(columns=col_list)
        print("columnas borradas")

#### Create Index
def set_index(self):
    try:
        data = data.rename_axis('index').reset_index()
    except Exception as exc:
        self.show_error(exc)

    

#### Encode data in column
def encode(self,column_name):
    try:
        data[column_name] = data[column_name].str.encode(encoding = 'utf8')
    except Exception as exc:
        self.show_error(exc)

  

#### Decode data in column
def decode(self,column_name):
    try:
        data[column_name] = data[column_name].str.decode(encoding = 'utf8')
    except Exception as exc:
        self.show_error(exc)
       

#### Split Column into separate columns
def split_column_new_columns(self, column_name_to_split:str,column_names:list):
    try:
        name = data[column_name_to_split].str.split(',',expand=True)
        name.columns = column_names
        data = pd.concat([data, name], axis=1)
        data = data.drop([column_name_to_split], axis=1)       

    except Exception as exc:
        self.show_error(exc)
    
    

#### Change data type of column
def change_data_type(self,column_name,data_type_name):
    try:
        data[column_name]  = data[column_name].astype(data_type_name)
    except Exception as exc:
        self.show_error(exc)
    
   

#### Get Max Value of Column
def max_(self,column_name):   
    try:
        maxs = data[column_name].max()
        return maxs
    except Exception as exc:
        self.show_error(exc)
    

#### Get Min Value of Column
def min_(self,column_name):
    try:
        min = data[column_name].min()
     
    except Exception as exc:
        self.show_error(exc)
    
  
def time_to_hit(self,column_name,column_name1):
    try:
        dia1 = data[column_name]
        dia2 = data[column_name1]
        
        hit = []
        
        for i,j in zip(dia1,dia2):
            i = datetime.strptime(i, '%d/%m/%Y')
            j = datetime.strptime(j, '%d/%m/%Y')
            diferencia = i - j
            hit.append(diferencia.days)
            
        df = pd.DataFrame(hit,columns =['days_to_hit'])
        print(df)
    except Exception as exc:
        self.show_error(exc)
    


def column_to_json(self,column_name):
    try:
        df = data[column_name].str.split(',',expand=True)        
        js=df.to_json()
        return js
    except Exception as exc:
        self.show_error(exc)
    

#### DF to XML
def to_xml(self,df):
    def row_xml(row):
        try:
            xml = ['<item>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</item>')
            
        except Exception as exc:
            self.show_error(exc)
        return '\n'.join(xml)
        
    res = '\n'.join(df.apply(row_xml, axis=1))
    return(res)




#### Save DF to CSV 
def save_data_csv(self, path):                   
    if data is not None:
        data.to_csv(path)

    


def show_error(self,ex):
    
    trace = []
    tb = ex._traceback_
    while tb is not None:
        trace.append({
                        "filename": tb.tb_frame.f_code.co_filename,
                        "name": tb.tb_frame.f_code.co_name,
                        "lineno": tb.tb_lineno
                        })
        
        tb = tb.tb_next
        
    print('{}Something went wrong:'.format(os.linesep))
    print('---type:{}'.format(str(type(ex)._name_)))
    print('---message:{}'.format(str(type(ex))))
    print('---trace:{}'.format(str(trace)))
import pandas as pd


def de_duplication(self):
        df = pd.read_excel('StaggingData.xlsx',sheet_name='Sheet1')
        df.head()
        df.drop_duplicates(subset=['Fname','Lname', 'Gender', 'Address', 'DOB'], keep='first', inplace=True)
        df.to_excel('DeDuplicationData.xlsx')
        return

def date_format_standardization(self):
        df = pd.read_excel('DeDuplicationData.xlsx',sheet_name='Sheet1')
        df2 = pd.DataFrame(df)
        df2['DOB'] = pd.to_datetime(df.DOB, errors='coerce')
        df2['DOB'] = df2['DOB'].dt.strftime('%e %B,%Y')
        df2.to_excel('DateFormatStandardization.xlsx')
        return
    
def derived_attribute_age(self):
        df = pd.read_excel('DateFormatStandardization.xlsx')
        df3 = pd.DataFrame(df)
        thisyear = pd.datetime.now().year
        df3a = df3.copy()
        df3a['DOB'] = pd.to_datetime(df3.DOB, errors='coerce')
        df3a['DOB'] = df3a['DOB'].dt.strftime("%Y")
        df3a.loc[(df3.DOB == 'NaT'), 'DOB'] =  None
        df3['Age'] = abs(thisyear - df3a['DOB'].astype(float))
        df3.to_excel('DerivedAttributeAge.xlsx')
        return
    
def split_single_attribute(self):
        df = pd.read_excel('DerivedAttributeAge.xlsx')
        df2 = pd.DataFrame(df)
        new = df2['Address'].str.split(", | ", n=1, expand=True)
        df2["Street"]= new[0] 
        df2["Colony"]= new[1] 
        new_1 = df2['Colony'].str.split(", | ", n=1, expand=True)
        df2["Colony"]= new_1[0] 
        df2["City"]= new_1[1]
        df2.drop(columns =["Address"], inplace = True)
        df2.to_excel('SplitSingleAttribute.xlsx')
        return
    
def merge_name_field(self):
        df = pd.read_excel('SplitSingleAttribute.xlsx')
        df2 = pd.DataFrame(df)
        df2['Full Name'] = (df2["Fname"] + " " + df2["Lname"])
        df2.drop(['Fname'], axis = 1, inplace = True)
        df2.drop(['Lname'], axis = 1, inplace = True)
        df2.to_excel('MergeNameField.xlsx')
        return
    
def decode_gender_field(self):
        df = pd.read_excel('MergeNameField.xlsx')
        df2 = pd.DataFrame(df)
        df2.loc[(df2.Gender == 'male') | (df2.Gender == 'Male') | 
                (df2.Gender == 'm') | (df2.Gender == 'M') | (df2.Gender == 1)
                , 'Gender'] = 'male'  
        df2.loc[(df2.Gender == 'female') | (df2.Gender == 'Female') | 
                (df2.Gender == 'f') | (df2.Gender == 'F') | (df2.Gender == 0)
                , 'Gender'] = 'female'  
        df2.to_excel('DecodeGenderField.xlsx')
        return
    
def delete_inconsistent_rows(self):
        df = pd.read_excel('DecodeGenderField.xlsx')
        df2 = pd.DataFrame(df)
        df2 = df2.drop(df2[(df2.Gender != 'male') & (df2.Gender != 'female')].index)
        df2.to_excel('DeleteInconsistentRows.xlsx')
        return
    
def summarization_1(self):
        df = pd.read_excel('DeleteInconsistentRows.xlsx')
        df2 = pd.DataFrame(df)
        df2 = df2.groupby('City')['Age'].sum()
        df2 = df2.rename( column={'Age':'Sum of Ages of Customer'}, inplace=True)
        df2.to_excel('output_1.xlsx')
        return
    
def summarization_2(self):
        df = pd.read_excel('DeleteInconsistentRows.xlsx')
        df2 = pd.DataFrame(df)
        df2 = df2.groupby('Age')['ID'].count()
        df2 = df2.rename(column={'ID':'Number of Customers'}, inplace=True)
        df2.to_excel('output_2.xlsx')




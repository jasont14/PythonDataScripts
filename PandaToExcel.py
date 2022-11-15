import pandas as pd

def save_df_to_excel(self,df,filename = None):
        try:
            if filename is not None:
               df.to_excel(filename , sheet_name = 'sheet', index=False)
            
        except Exception as exc:
            self.show_error(exc)
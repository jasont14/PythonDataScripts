import chardet
import os
import shutil
import glob
import pandas as pd

def check_used_space(self,path):
    try:
        total_size = 0
        
        #use the walk() method to navigate through directory tree
        for dirpath, dirnames, filenames in os.walk(path):
            for i in filenames:
                
                #use join to concatenate all the components of path
                f = os.path.join(dirpath, i)
                
                #use getsize to generate size in bytes and add it to the total size
                total_size += os.path.getsize(f)
        
        self.bytes = total_size
        total_size = self.formatSize()

        return total_size
    
    except Exception as exc:
        self.show_error(exc)

def check_free_space(self,path_data):
    try:
        self.bytes = shutil.disk_usage(str(path_data))[2]
        free_space = self.formatSize()
        print('Espacio libre en disco: {}'.format(free_space))
    
    except Exception as exc:
        self.show_error(exc)

def check_path(self,path_check):       
    self.dir_exist = os.path.exists(path_check)

def get_lst_files(self,path_data,tipo):    
    try:
        self.lst_files = [f for f in glob.glob(str(path_data)+'/**/*.'+ tipo.lower(), recursive=True)]
        
    except Exception as exc:
        self.show_error(exc)

def get_data_csv(self, the_path):
    
    try:
        self.data = pd.read_csv(the_path)
        
    except Exception as exc:
        self.show_error(exc)

def get_data_csv_nozip(self, the_path):
    try:
        with open(the_path, 'rb') as fx:
            result = chardet.detect(fx.read()) 
            #chardet is 'univerisal Character Detector' pypi
            
        child = os.path.splitext(os.path.basename(the_path))[0]
        print('File: {} - {}'.format(child,result))
        self.data = pd.read_csv(the_path
                            )
        
    except Exception as exc:
        self.show_error(exc)

def show_error(self,ex):
    
    trace = []
    tb = ex.__traceback__
    while tb is not None:
        trace.append({
                        "filename": tb.tb_frame.f_code.co_filename,
                        "name": tb.tb_frame.f_code.co_name,
                        "lineno": tb.tb_lineno
                        })
        
        tb = tb.tb_next
        
    print('{}Something went wrong:'.format(os.linesep))
    print('---type:{}'.format(str(type(ex).__name__)))
    print('---message:{}'.format(str(type(ex))))
    print('---trace:{}'.format(str(trace)))
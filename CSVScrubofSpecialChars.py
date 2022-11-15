import pandas as pd

write_file = '~/directory/filename.csv'
df = pd.read_csv(write_file)
df = df.replace({'\$':''}, regex = True)
df = df.replace({'%':''}, regex = True)
df = df.replace({'\,':''}, regex = True)
df = df.replace({"'":''}, regex = True)
df = df.replace({"nan":''}, regex = True)
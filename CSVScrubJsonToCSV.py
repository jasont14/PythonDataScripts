import requests
import json



##### API URL and URL PARAMETERS GO HERE #####
params = {'######':'######'}
url = 'request_url'


##### CREATE AN EMPTY LIST TO STORE THE JSON DATA #####
table = []

##### MAKE THE REQUEST AND THEN PUT THE REQUEST DATA INTO JSON FORMAT #####
r = requests.get(url, params=params)
data = r.json()

##### LOOP THROUGH EACH JSON OBJECT IN THE LIST AND PUT IT CLEANLY INTO ITS OWN ROW  #####
for item in data['key_where_the_data_lives']:
  ### item.keys() (to figure out what the keys are)
  row = [
  item.get('key1'),
  item.get('key2'),
  item.get('key3'),
  item.get('key4'),
  item.get('key5'),
  item.get('keyN')
  ]
  table.append(row)
  
  
##### WRITE THE ROWS OF THE LIST (TABLE) INTO A CSV FILE ######  
write_file = '~/directory/filename.csv'
with open(write_file,'w', newline = '') as f:
    writer = csv.writer(f, lineterminator = '\n')
    writer.writerows(table)
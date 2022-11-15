import requests
import json
import csv



#### PULLING FROM A SYNCHRONOUS ENDPOINT 

endpoint = '#######'
url = f'https://place.com/v11.0/{endpoint}/insights' 
r = requests.get(url,params=params) 
apiResults = r.json()


data = []

while(True):
	try:
		for row in apiResults['data']:
			data.append(row)
		# Attempt to make a request to the next page of data, if it exists.
		apiResults=requests.get(apiResults['paging']['next']).json()
	except KeyError:
		# When there are no more pages (['paging']['next']), break from the
		# loop and end the script.
		break
          
#### PULLING FROM A ASYNCHRONOUS ENDPOINT (REQUEST IS PROCESSED IN THE BACKGROUND)     
          
endpoint = '#######'
url = f'https://place.com/v11.0/{endpoint}'
r = requests.post(url,params=params)
if r.status_code != 200:
	print(f'{r.status_code} error with request: {r.text}\nExiting the program ...')
	raise SystemExit
apiResults = r.json()
print(apiResults)

report_run_id = campaigns.get('report_run_id')
job_status = None

while job_status != 'Job Completed':

		params = {
	            'access_token':'############'
	        }

		url = f'https://place.com/v11.0/{report_run_id}'
		r = requests.get(url,params=params)
		apiResults = r.json()
		job_status = apiResults.get('status')
		if job_status == 'Job Completed':
			print('Job completed...breaking the loop and retrieving the data')
			break
		else:
			print('Job not completed....percent completed: {}'.format(results.get('percent_completion')))
			time.sleep(30)


url = f'https://place.com/v11.0/{report_run_id}'
r = requests.get(url,params=params)
apiResults = r.json()
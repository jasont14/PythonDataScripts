import smtplib
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import traceback

#### THIS IS THE FUNCTION THAT WILL USE SMTPLIB TO SEND EMAILS VIA PYTHON ####
def send_alert(subject,msg,receivers) -> None:
	msg = MIMEText(msg,'html')
	# if '@microsoft.graph.downloadUrl' in files.keys():
	msg['Subject'] = subject
	msg['From'] = USER
	msg['To'] = ','.join(receivers)
	# Send the message via our own SMTP server.
	try:
		s = smtplib.SMTP('smtp.gmail.com','587')
		s.starttls()
		s.login(USER,PASSWORD)
		s.send_message(msg)
		s.quit()
	except smtplib.SMTPException as e:
		print("Error: unable to send email: {}".format(e))

#### INPUT THE EMAIL USER NAME AND PASSWORD AND WHO SHOULD RECEIVE THE EMAIL HERE ####
USER = 'USER'
PASSWORD = 'password'
RECIEVERS = ['reciever1','reciever2',[n]....]

def some_function() -> None:
    pass
#### THIS IS YOUR MAIN CODE CHUNK OR FUNCTION WITH TRY AND EXCEPT CRITERIA
try:
   some_function()
except Exception as e:
  tb = traceback.format_exc()
  subject = 'There was an error on the script'
  msg = f'Here is the full traceback: {tb}'
  send_alert(subject,msg,RECIEVERS)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from vid_cap import vid_capt
import time

def sendmail():
    
    email_user = 'pytester.py@gmail.com'#server email address
    email_password = 'pypypy12' #server email password
    email_send = 'aakashguru6898@gmail.com' #email address of owner or authority
    
    print('User not recognized...')
    vid_capt()
    print("Sending Mail....")
    
    #time.sleep(5)
    
    #print('Email Sent Successfully...')
    
    subject = 'Check out, someone is knocking your door'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = 'Reply "Allow" to open the door, or "Deny" to leave door to be closed'
    msg.attach(MIMEText(body,'plain'))

    filename = 'output.mp4'
    attachment = open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.close()
    print('Email Sent Successfully...')
#sendmail()'''

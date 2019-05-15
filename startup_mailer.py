import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText
import datetime
to="roberto.buelvas@mail.mcgill.ca"
gmail_user="mac.robotics01@gmail.com"
gmail_password="iloverobots123"
smtpserver=smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today=datetime.date.today()
arg="ip route list"
p=subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
data=p.communicate()
split_data=data[0].split()
ipaddr=split_data[split_data.index("src")+1]
mail_body="IP address: %s" % ipaddr
msg=MIMEText(mail_body)
msg["Subject"]="RPi@"+ipaddr+" started up on %s" % today.strftime("%d %b %Y")
msg["From"]=gmail_user
msg["To"]=to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()

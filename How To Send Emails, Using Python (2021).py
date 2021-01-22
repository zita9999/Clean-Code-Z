
#---How To Send Emails, Using Python (2021)---


##################################### -Importing Necessary Libraries- #############################################

import smtplib, ssl
from email.mime.text import MIMEText


##################################### -Sender, Reciever, Body of Email- #############################################

#Input the the email address of who you want to send the email
sender = 'your_email@email.com'
#Input the the email address's of those you want to receive the email
receivers = ['recipient1@recipient.com', 'recipient2@recipient.com']
#input the body of text you want in your email
body_of_email = 'Text to be displayed in the email'


##################################### -Creating the Message, Subject line, From and To- #############################################

#Creates the inital messgae
msg = MIMEText(body_of_email, 'html')
#Input subject line of your email
msg['Subject'] = 'Subject line goes here'
#From the email addresses you put in the last section those will be the From and To's
msg['From'] = sender
msg['To'] = ','.join(receivers)

##################################### -Connecting to Gmail SMTP Server- #############################################

#Connects to the Gmail server
s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
#After it connects you need to put your login details so it can access your Gmail account
s.login(user = 'your_username', password = 'your_password')
#It will offically send the email
s.sendmail(sender, receivers, msg.as_string())
s.quit()
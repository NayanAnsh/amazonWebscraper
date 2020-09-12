# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 20:41:12 2020

@author: Nayan
"""

import smtplib as smt
from email.message import EmailMessage

HTML = '''\
    <!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>
<p>My first paragraph.</p>

</body>
</html>
    '''
def sendMails(Subject,body):
    
    
    fromMsg = "nezukodemon89@gmail.com"
    toMsg = ["nayanansh@gmail.com"
             ,"nayanansh69@gmail.com"
             ]
          
    
    msg = EmailMessage()
    msg['Subject'] = Subject
    msg['from'] =  fromMsg
    msg['To'] = ",".join(toMsg)
    msg.set_content(body)
    msg.add_alternative(HTML , subtype = 'html')
    message = Subject+"\n"+body+"\n"
    print(message)
    
    server = smt.SMTP("smtp.gmail.com",587)
    server.starttls() # Enable TLS
    server.login("nezukodemon89@gmail.com","AsamplePass@12345")
    server.set_debuglevel(1) #Print Data level 1 at lvl2 print data with time stamp at lvl 0 nothing will be printed
    server.send_message(msg)
    server.quit()
sendMails("Subject : I am your amazon bot hello!! ","I am working correctly please set debug lvl to 1 or 2 for more data")
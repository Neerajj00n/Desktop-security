#!/usr/bin/python
import pygame
import pygame.camera
import smtplib
import time
import crypt
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import imapclient
import pyzmail
import os
import urllib2


def photo(image): # This function will Capture image
	pygame.camera.init()
	cam = pygame.camera.Camera("/dev/video0", (640,480))
	cam.start()
	img = cam.get_image()
	pygame.image.save(img, image)
	cam.stop()
	return img

def email(image, fromaddr , toaddr, password): # This will send that image to email<toaddr>
 	
	msg = MIMEMultipart() 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Security"
	 
	body = "This guy tried to acessed your laptop at {}".format(time.ctime())
	 
	msg.attach(MIMEText(body, 'plain'))
	 
	filename = image
	attachment = open(image, "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def Action(fromaddr, toaddr, password): # This Function will read the Emails of <fromaddr> and take action according to your email.

	codes = ["Shutdown", "Changepass",]
	imap = imapclient.IMAPClient('imap.gmail.com', ssl=True)
	imap.login(fromaddr , password)
	imap.select_folder('INBOX', readonly=False)
	loop = 1
	while (loop == 1):
		
		UIDs = imap.search("ALL")
		rawMessages = imap.fetch(UIDs[-1:], ['BODY[]'])
		message = pyzmail.PyzMessage.factory(rawMessages[UIDs[-1]][b'BODY[]'])
		msg = message.text_part.get_payload().decode(message.text_part.charset)
		pymsg = msg.strip()
		
		if pymsg == codes[0]: # This will simply shutdown your pc
			imap.delete_messages(UIDs[-1])
			imap.expunge()			
			os.system("/sbin/shutdown now")
			loop = 0
			
		elif pymsg == codes[1]: #This will change the password of login user and then shutdown your pc
			newpassword= "akatsuki" #give New password here 
			username = os.getlogin()
			imap.delete_messages(UIDs[-1])
			imap.expunge()
			userPasswd(username, newpassword)			
			os.system("/sbin/shutdown now")
			loop = 0
		else:
			 pass
			 
def userPasswd(username, newpassword):
	encPass = crypt.crypt(newpassword,"22")
	command = "/usr/sbin/usermod -p '{0:s}' {1:s}".format(encPass, username)
	result = os.system(command)

######################################################################
#this is for checking internet connection before runing rest of the code
loop_value = 1

while (loop_value == 1):

    try:

        urllib2.urlopen("https://www.google.com/",  timeout=1)

    except urllib2.URLError, e:
			pass  

    else:

        print "Up and running."

        loop_value = 0

#######################################################################

fromaddr = "fromaddr@gmail.com" #The address you wanna send email from
toaddr = "toaddr@gmail.com" # The address u will recive email into 
image = "/home/neerajjoon/%s.jpg" % time.ctime() #Change /home/neerajoon/ with /home/<yourusername>
password ="Eminem" #password for fromaddr

photo(image)
email(image , fromaddr , toaddr, password)
Action(fromaddr, toaddr, password)

############################################################################
#
# AUTHOR        : Lebougui
# DESCRIPTION   : v0.1 -Send mail with Subject, From, To, CC, Message, 
#                       Message part in html format (htm_file),
#                       and attached files elements

#############################################################################

import smtplib
import os
import sys

import email
from email import *
from email.MIMEMultipart import *
from email.Utils import COMMASPACE,formatdate
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase

def SendMail(SMTP="", Subject="", From="", To=[], CC=[], Message="", html_file="", Files=[]):

        """
        ----------------------------------------------------------------------------------

        Send a mail using SMTP address.
        Usage : SendMail (SMTP, From, To, Message, [Subject, CC, html_file, files])
        Parameters "SMTP", "From", "To" and "Message" are necessary.
        "Subject", "C"C, "html_file" and "files" are optionnal.
        
        To send an e-mail in html format you can use "html_file" option.
        By default To and CC parameters are composed by mail addresses.
        
        To send mails to alias To and CC parameters must have 2 sub-lists.
        
        To or CC = [ [receiver_list] , [header_list ].
        receiver_list is composed by al the elementary mail addresses.
        header_list is composed by alias.

        ----------------------------------------------------------------------------------

        """ 

        if SMTP == "":
                print "Error : SMTP is empty"
                sys.exit(1)
        if From == "":
                print "Error : From address is empty"
                sys.exit(1)
        if To == []:
                print "Error : To address is empty"
                sys.exit(1)
        if Message == "":
                print "Error : Message is empty"
                sys.exit(1)

        if type(To[0]) == list and type(To[1]) == list :
                To_header="; ".join(To[1])
                To_receiver="; ".join(To[0])
        else:
                To_header=To_receiver="; ".join(To)

        if type(CC[0]) == list and type(CC[1]) == list :
                CC_header="; ".join(CC[1])
                CC_receiver="; ".join(CC[0])
        else:
                CC_header=CC_receiver="; ".join(CC)

        msg = MIMEMultipart()
        msg['From'] = From
        msg['Date'] = formatdate(localtime=True)
        msg['To'] = To_header

        if CC != "" : 
                msg['CC'] = CC_header

        msg['Subject'] = Subject

        if html_file != "":
                temp= open(html_file, 'rb')
                msg.attach( MIMEText(Message+temp.read() , 'html'))
                temp.close()
        else:
                msg.attach( MIMEText(Message))

        #Attach all the files into mail
        if len(Files)>0:
                for my_file in Files:
                        if (os.path.isfile(my_file)) :
                                part = MIMEBase('application', "octet-stream")
                                part.set_payload( open(my_file,"rb").read() )
                                Encoders.encode_base64(part)
                                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(my_file))
                                msg.attach(part)
                        else:
                                print 'Error : File ' + my_file + ' does not exist.'

        ##For Debug only
        #print "-->SMTP: %s \r\n\r\n-->From : %s \r\n\r\n-->To: %s \r\n\r\n-->To_h: %s \r\n\r\nSubject: %s \r\n\r\n-->Files: %s \r\n\r\n-->To_s: %s \r\n\r\n-->Message: %s" % (SMTP, From, To, To_header, Subject, Files, To_receiver, msg.as_string())

        #####   Send notification mail   #####
        ## Connect to SMTP server
        try:
                mailServer = smtplib.SMTP(SMTP)
        except:
                print 'Error : SMTP connexion failed'
                sys.exit(1)

        ## Send mail
        try:
                mailServer.sendmail(From, To[0] , msg.as_string())
        except:
                print 'Error : Could not send mail '
                sys.exit(1)

        ## Quit
        try:
                mailServer.quit()
        except:
                print 'Error : Could not exit properly'
                sys.exit(1)


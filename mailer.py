#
#  AUTHOR        : Lebougui
#  DESCRIPTION   : v-0.1 -Send mail to all resolver of PCRs in "assigned", "entered",
#                       "modified", "resolved" status.
#                       -Adding "status" flag
#                       -Adding the VM name and generation date in the mail for resolver 
#                       of "resolved" PCRs in order to close them (already embedded in VM delivery)
#                       -Adding the config file use about settings
#                       -Ading the absolute mail.conf location
#                 v-0.2 -Adding the html message format support
#                       -Improving mailing process regarding config file.
#                       -Adding alias mail address support
#############################################################################

#import the mailer module
from sendmail import *

#import the needed modules
import ConfigParser
import sys
import string
import tempfile, shutil, os
import csv
import getopt

def get_subject(tag):

        """
        ----------------------------------------------------------------------------------
        Get the subjcet from config file
        ----------------------------------------------------------------------------------
        """ 
        return config.get(tag, 'Subject')

def get_message(tag):

        """
        ----------------------------------------------------------------------------------
        Get the message from config file
        ----------------------------------------------------------------------------------
        """ 
        return config.get(tag, 'Message')

def get_from(tag):

        """
        ----------------------------------------------------------------------------------
        Get the from mail address from config file
        ----------------------------------------------------------------------------------
        """ 
        return config.get(tag, 'From') + str(get_domain())


def get_to(tag):

        """
        ----------------------------------------------------------------------------------
        Get the tracker "to" list from config file
        To take into account outlook alias the "to" list must be composed by 2 sub-lists.
        "receiver" and "header". The "receiver" list is like the "header" one but the alias
        are replaced by their content.
        To = [ [receiver_list] , [header_list] ]
        ----------------------------------------------------------------------------------
        """ 

        temp0=[]
        temp1=[]
        for i in string.split(config.get(tag, 'To')):

                if (config.has_option('ALIAS', i)):
                        for j in string.split(config.get('ALIAS', i)):
                                temp0.append(j+str(get_domain()))
                else:
                        temp0.append(i+str(get_domain()))
                temp1.append(i+str(get_domain()))

        temp=[]
        temp.append(temp0)
        temp.append(temp1)

        return temp



def get_domain():
        """
        ----------------------------------------------------------------------------------
        Get the domain from config file
        ----------------------------------------------------------------------------------
        """ 

        return config.get('NETWORK', 'Domain')


def get_smtp():

        """
        ----------------------------------------------------------------------------------
        Get the SMTP address from config file
        ----------------------------------------------------------------------------------
        """ 

        return config.get('NETWORK', 'Smtp')


def get_cc(tag):

        """
        ----------------------------------------------------------------------------------
        Get the tracker "CC" list from config file
        To take into account outlook alias the "CC" list must be composed by 2 sub-lists.
        "receiver" and "header". The "receiver" list is like the "header" one but the alias
        are replaced by their content.
        To = [ [receiver_list] , [header_list] ]
        ----------------------------------------------------------------------------------
        """ 
        temp0=[]
        temp1=[]

        for i in string.split(config.get(tag, 'CC')):
                if (config.has_option('ALIAS', i)):
                        for j in string.split(config.get('ALIAS', i)):
                                temp0.append(j+str(get_domain()))
                else:
                        temp0.append(i+str(get_domain()))
                temp1.append(i+str(get_domain()))

        temp=[]
        temp.append(temp0)
        temp.append(temp1)

        return temp



if __name__ == '__main__':
        config = ConfigParser.ConfigParser()
        config.read(os.path.dirname(sys.argv[0]) + '/mailer.conf')

        options, remainder = getopt.getopt(sys.argv[1:], 't:m:f:', ['tag=', 'message=','files='])

        if (len(options) == 0 ):
                print "Syntax is: %s -t <tag> [-m <message>] [-f <file1,file2,...>]" % (sys.argv[0])
                sys.exit(1)
        else:
            Files=[]
            for opt, arg in options:
                if opt in ('-t', '--tag'):
                    From = get_from(arg)
                    To = get_to(arg)
                    CC = get_cc(arg)
                    Subject = get_subject(arg)
                    Message = get_message(arg)
                elif opt in ('-m', '--message'):
                    Message = arg
                elif opt in ('-f', '--files'):
                    Files = arg.split(',')
                        
                    for entry in Files:
                       if (os.path.isfile(entry) == False):
                           print "Error : File %s does not exist." % (entry)
                           sys.exit(1)

            #Send mail
            if len(Files) == 0:
                SendMail(get_smtp(), Subject, From, To, CC, Message, "")
            else:
                SendMail(get_smtp(), Subject, From, To, CC, Message, "", Files)


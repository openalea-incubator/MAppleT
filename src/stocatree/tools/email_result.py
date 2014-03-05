#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KELNER
#
# Created:     14/01/2011
# Copyright:   (c) KELNER 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import smtplib

'''
drct: directory of the result file
rst: name of the result file
rcvr: email address of the result receiver
'''
#def email(drct, rst, rcvr):
def email(rcvr):
    account = 'stocatree@gmail.com'
    security_code = 'stocatree++'
    host = 'smtp.gmail.com'
    port = 587

    message = "Experiment finished"

    #attachment_list = [drct + rst]

    sender_address = account
    receiver_address = rcvr

    handle = smtplib.SMTP(host, port)
    handle.ehlo()
    handle.starttls()
    handle.ehlo()
    handle.login(account, security_code)
    handle.sendmail(sender_address, receiver_address, message)
    #handle.sendmail(sender_address, receiver_address = 'han@supagro.inra.fr')
    #handle.close()
    handle.quit()


def main():
    email()

if __name__ == '__main__':
    email()

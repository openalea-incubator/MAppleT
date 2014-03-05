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
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import mimetypes
from email import encoders

'''
drct: directory of the result file
rst: name of the result file
rcvr: email address of the result receiver
strt_d: starting date of the experiments
nd_d: ending date of the experiments
exp_nbr: number of experiments supposed to be implemented
sccfl_nbr: number of experiments successful
cpl: a flag for whether the batchmode experiment is completed or not
'''
def email(drct, rst_lst, rcvr, strt_d, nd_d, exp_nbr, sccfl_nbr, cpl):

#def email():
#    drct = "Batchmode_ExpCounters&Results/"
#    rst_lst = ['light_interception_per_shoot.csv', 'light_interception_observ.csv', 'light_interception.csv']
#    rcvr = 'han@supagro.inra.fr,stocatree@gmail.com'
#    strt_d = '1996'
#    nd_d = '1997'
#    exp_nbr = 10
#    sccfl_nbr = 10
#    cpl = True

    account = 'stocatree@gmail.com'
    security_code = 'stocatree++'
    host = 'smtp.gmail.com'
    port = 587

    # to initialise the attachment list
    attachment_list = []

    message = MIMEMultipart()

    if cpl == 1:
        message['Subject'] = "Batchmode completed, started from %s to %s" % (strt_d, nd_d)
        Text = "This is an automatic email. Attached is the result. \n \n \
                Starting Date: %s \n \
                Ending Date: %s \n \
                Number of Planned Experiments: %u \n \
                Number of Successful Experiments: %u \n \
                " % (strt_d, nd_d, exp_nbr, sccfl_nbr)
        message.attach(MIMEText(Text))
        for i in range(len(rst_lst)):
            result_file = drct + rst_lst[i]
            attachment_list.append(result_file)
            #attachment_list = [drct + rst]
        if len(attachment_list) > 0:
            for filename in attachment_list:
                ctype, encoding = mimetypes.guess_type(filename)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)

                fp = open(filename, 'rb')
                part = MIMEBase(maintype, subtype)
                attach_content = fp.read()
                part.set_payload(attach_content)
                fp.close()
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(part)
    elif cpl == 2:
        message['Subject'] = "Btachmode results cannot be emailed"
        Text = "Maybe the reult file is too big. \n \
                Please have a check."
        message.attach(MIMEText(Text))
    else:
        message['Subject'] = "Btachmode simulation has been broken"
        Text = "This is an automatic email. The exerpiment has been broken. \n \
                Please have a check."
        message.attach(MIMEText(Text))
        for i in range(len(rst_lst)):
            result_file = drct + rst_lst[i]
            attachment_list.append(result_file)
            #attachment_list = [drct + rst]
        if len(attachment_list) > 0:
            for filename in attachment_list:
                ctype, encoding = mimetypes.guess_type(filename)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)

                fp = open(filename, 'rb')
                part = MIMEBase(maintype, subtype)
                attach_content = fp.read()
                part.set_payload(attach_content)
                fp.close()
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(part)

    """
    Text = "This is an automatic email. Attached is the result. \n \n \
            Starting Date: %s \n \
            Ending Date: %s \n \
            Number of Planned Experiments: %u \n \
            Number of Successful Experiments: %u \n \
            " % (strt_d, nd_d, exp_nbr, sccfl_nbr)
    """
    """
    message.attach(MIMEText(Text))

    for i in range(len(rst_lst)):
        result_file = drct + rst_lst[i]
        attachment_list.append(result_file)
        #attachment_list = [drct + rst]

    if len(attachment_list) > 0:
        for filename in attachment_list:
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            fp = open(filename, 'rb')
            part = MIMEBase(maintype, subtype)
            attach_content = fp.read()
            part.set_payload(attach_content)
            fp.close()
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(part)
    """
    sender_address = account
    receiver_address = rcvr

    handle = smtplib.SMTP(host, port)
    handle.ehlo()
    handle.starttls()
    handle.ehlo()
    handle.login(account, security_code)
    handle.sendmail(sender_address, receiver_address, message.as_string())
    handle.quit()


def main():
    email()

if __name__ == '__main__':
    email()

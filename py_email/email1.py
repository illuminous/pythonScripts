###Set up imports
import sys, os, re
message1 = "section 1 failed"
message2 = "section 2 failed"
message3 = "this worked"

"""This script sends an email message to your email account.
"""
SMTPserver = 'smtp.gmail.com'
sender =     'jherynk.smtp@gmail.com'
destination = ['jherynk.sem@gmail.com']

USERNAME = "jherynk.smtp"
PASSWORD = "pythongo!"

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


##content="""\
##The stage 1 script has completed runs for your project.
##"""

content = message1 + '\n' + message2 + '\n' + message3
subject="Sent from Python"


from ssmtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.MIMEText import MIMEText

try:
    msg = MIMEText(content, text_subtype)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception, exc:
    sys.exit( "mail failed, check smtp email compatibility; %s" % str(exc) )

import email, imaplib, time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'devletter.settings'

from django.conf import settings

#takes Letter and UserProfile and returns a MIME formatted message
def pack_MIME(letter, user_profile):
    mail = MIMEMultipart('alternative')
    mail['Subject'] = letter.template.subject.format(**{'game':letter.game.name})
    mail['From'] = settings.ROBOT_MAILER
    mail['To'] = letter.developer.email
    message = letter.template.template.format(**{
    'game':    letter.game.name,
    'devname': letter.developer.name,
    'text1':   letter.text1,
    'text2':   letter.text2,
    'sig':     user_profile.signature,
    })
    body = MIMEText(message, 'html', 'UTF-8')
    mail.attach(body)

    return mail

def send_draft(mail):
    #probably should be a setting and not hardcoded, but eh
    server = imaplib.IMAP4_SSL('imap.gmail.com', port = 993)
    server.login(settings.ROBOT_MAILER, settings.ROBOT_PASSWORD)
    server.select('[Gmail]/Drafts')
    #this is a prime example of 'magic' at work
    #I believe it's taking a MIME object, turning it into a string, then back into a mail object, then back into a string.
    #it could probably be reduced a few steps
    #like, I know what it's doing, but I don't really *know*, y'know?
    server.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), str(email.message_from_string(mail.as_string())))    

    server.close()
    server.logout() 

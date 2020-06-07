import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import configparser 
import logging

# Setup logger
logger = logging.getLogger(__name__)

def send_email(receiver_email,
               email_subject,
               email_message,
               attachment_location=''):

    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.join( os.path.dirname(os.path.realpath(__file__)), 'config.ini'))

    smtp_server = config.get('EMAIL', 'SMTP_SERVER')
    smtp_server_port = config.get('EMAIL', 'SMTP_Port')
    sender_email = config.get('EMAIL', 'SENDER_EMAIL')
    sender_pass = ''

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        logger.info (f"Using SMTP Server {smtp_server} and sender_email {sender_email}")

        #Create SMTP session for sending the mail
        session = smtplib.SMTP(smtp_server, smtp_server_port)
        session.starttls() #enable security
        session.login(sender_email, sender_pass) #login with mail_id and password
        text = msg.as_string()
        session.sendmail(sender_email, receiver_email, text) #Sensitive
        session.quit()
        logger.info(f'Email sent to {receiver_email} successfully')
        print('Mail Sent')

    except Exception as e:
        logger.info(e)
        print('Something wrong')
        return False

    return True

              
if __name__ == "__main__":

    file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"get_name.sql")
    print (send_email("someone@gmail.com", "test", "This is a test", file)) # sensitive

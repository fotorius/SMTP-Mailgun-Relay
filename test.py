import smtplib
from email.mime.text import MIMEText

SMTP_PORT = 25
SMTP_HOST = 'localhost'
SENDER = 'user@example.com'
RECIPIENTS = ['user@example.com']
SUBJECT = 'Test Email'
BODY = 'This is a test email.'

def send_email():

    msg = MIMEText(body)
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = ', '.join(RECIPIENTS)

    # Connect to the local SMTP server
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail(SENDER, RECIPIENTS, msg.as_string())

    return 'Email sent!'

if __name__ == '__main__':
    send_email()

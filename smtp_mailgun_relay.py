"""
SMTP Mailgun Relay Server

This is a script that allows yo to send emails from your local server to other
receipients using the Mailgun sevice.

Why? Some service providers are starting to block SMTP ports (25, 465, and 587)
due to abuse. This system allows you to use a local SMTP server and relays them
to Mailgun using their own REST API.

Requirements:
- Python 3.x
- pip -r reqs.txt

Usage:
1. Replace 'MAILGUN_API_KEY' with your Mailgun API key.
2. Replace 'MAILGUN_API_URL' with your Mailgun url "https://api.mailgun.net/v3/<YOUR DOMAIN>/messages".
3. Run the script:
    python smtp_mailgun_relay.py
4. Configure your other services to point to your HOSTNAME and your SMTP_PORT.

Testing:
- Using "mail" run on the terminal: 
    echo "This is a test email." | mail -s "Test Email" recipient@your-domain.com
"""

import os
import json
import logging
import asyncio
import requests
import datetime

from aiosmtpd.controller import Controller
from email import message_from_bytes
from dotenv import load_dotenv

load_dotenv()

SMTP_PORT = os.getenv('SMTP_PORT','25')
HOSTNAME = os.getenv('HOSTNAME','localhost')
FROM_ADDRESS = os.getenv('FROM_ADDRESS',None)
MAILGUN_API_URL = os.getenv('MAILGUN_API_URL')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.WARNING)

class SMTPHandler:

    async def handle_DATA(self, server, session, envelope):
        # Parse the email content
        email_message = message_from_bytes(envelope.content)

        # Extract relevant fields
        from_address = FROM_ADDRESS or envelope.mail_from
        to_addresses = envelope.rcpt_tos
        subject = email_message['Subject']

        body = ""
        html_body = None

        # Check if the email is multipart
        if email_message.is_multipart():
            # Iterate through the parts
            for part in email_message.walk():
                # Check if the part is text/plain or text/html
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True)
                    if body is not None:
                        body = body.decode()
                elif content_type == 'text/html':
                    # Optionally handle HTML part if needed
                    html_body = part.get_payload(decode=True)
                    if html_body is not None:
                        html_body = html_body.decode()
                    # You can choose to use html_body instead of body if desired
        else:
            # If not multipart, get the payload directly
            body = email_message.get_payload(decode=True)
            if body is not None:
                body = body.decode()

        data={
            'from': from_address,
            'to': to_addresses,
            'subject': subject,
            'text': body,
            'html': html_body,
        }

        # Log the interaction
        logging.info(f'{from_address} {to_addresses} {subject}')

        try:
            # Connect to Mailgun server
            resp = requests.post(
                MAILGUN_API_URL,
                auth=('api', os.getenv('MAILGUN_API_KEY')),
                data=data
            )
        
            if resp.status_code == 200:
                logging.info(f'Successfully sent an email to "{to_addresses}" via Mailgun API.')
                return '250 Message accepted for delivery'
            else:
                logging.warning(f'Could not send the email, reason: {resp.text}')
                return '451 4.4.1 IMAP server unavailable'

        except Exception as e:
            logging.error(f'Mailgun error: {e}')
            return '421 Service not available'

async def main():
    controller = Controller(SMTPHandler(), hostname=HOSTNAME, port=SMTP_PORT)
    controller.start()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())

# smtp_server.py
import os
import json
import logging
import asyncio
import requests

from aiosmtpd.controller import Controller
from email import message_from_bytes
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

SMTP_PORT = os.getenv('SMTP_PORT','25')
HOSTNAME = os.getenv('HOSTNAME','localhost')
FROM_ADDRESS = os.getenv('FROM_ADDRESS',None)
MAILGUN_API_URL = os.getenv('MAILGUN_API_URL')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        # Parse the email content
        email_message = message_from_bytes(envelope.content)

        # Extract relevant fields
        from_address = FROM_ADDRESS or envelope.mail_from
        to_addresses = envelope.rcpt_tos
        subject = email_message['Subject']
        body = email_message.get_payload(decode=True).decode()

        if to_addresses:
            to_address = to_addresses[0]
            data={
                'from': from_address,
                'to': to_address,
                'subject': subject,
                'text': body,
            }
            print(from_address,to_addresses,subject)
            try:
                resp = requests.post(
                    MAILGUN_API_URL,
                    auth=('api', os.getenv('MAILGUN_API_KEY')),
                    data=data
                )
            
                if resp.status_code == 200:
                    print(f"Successfully sent an email to '{to_address}' via Mailgun API.")
                    return '250 Message accepted for delivery'
                else:
                    print(f"Could not send the email, reason: {resp.text}")
                    return '451 4.4.1 IMAP server unavailable'
            except Exception as e:
                print(f"Mailgun error: {e}")
                return '421 Service not available'
        else:
            print(f"Invalid to email")
            return '500 invalid to email'

async def main():
    controller = Controller(CustomSMTPHandler(), hostname=HOSTNAME, port=SMTP_PORT)
    controller.start()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())


# SMTP Mailgun Relay

This is a script that allows yo to send emails from your local server to other
receipients using the Mailgun sevice.

Why? Some service providers are starting to block SMTP ports (25, 465, and 587)
due to abuse. This system allows you to use a local SMTP server and relays them
to Mailgun using their own REST API.

## Requirements

- Docker >= 26.1.3

## .env

```
SMTP_PORT = 25
HOSTNAME = "localhost"
FROM_ADDRESS = "user@example.com"
MAILGUN_API_URL = "https://api.mailgun.net/v3/<YOUR DOMAIN>/messages"
MAILGUN_API_KEY = "xxxxxxxxxxxxxxxxxxxx"
```

## Docker

```
docker build --tag "smtp_gunmail_relay" .
docker run -d --name smtp_gunmail_relay -p 127.0.0.1:25:25 smtp_gunmail_relay # Set your port
```

## Testing

Using "mail" run on the terminal: 

```
echo "This is a test email." | mail -s "Test Email" recipient@your-domain.com
```

Using the provided test.py file: Set your own variables at the beginning of the file and run it.

```
python test.py
```

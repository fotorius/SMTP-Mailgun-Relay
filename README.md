# SMTP Mailgun Relay

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
docker run -p 127.0.0.1:25:25 smtp_gunmail_relay
```


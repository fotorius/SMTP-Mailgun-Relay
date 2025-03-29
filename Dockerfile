FROM python:3.13-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY . .
RUN pip install -r reqs.txt
EXPOSE ${SMTP_PORT}
CMD ["python","smtp_server_relay.py"]

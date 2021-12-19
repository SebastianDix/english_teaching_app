#!/usr/bin/env python3
import requests
import os
from typing import List
from requests import Response, post

class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message

class Mailgun:
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)

    FROM_TITLE = 'Pricing service'
    FROM_EMAIL = "postmaster@sandbox15453512c55b422d8650b8f41ecefeba.mailgun.org"

    @classmethod
    def send_mail(cls,email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException('Failed to load Milgun API key.')
        if cls.MAILGUN_DOMAIN is None:
            raise MaiulgunException('Failed to load Mailgun domain.')

        response = post(
            f"{cls.MAILGUN_DOMAIN}/messages",
            auth=("api",cls.MAILGUN_API_KEY),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            print(response.json())
            raise MailgunException('An error occurred while sending e-mail.')
        return response

#Mailgun.send_mail('sebastiandix3@gmail.com','Funky guitars','Yeah buy these funky funky guitars','<h1>Spank this</h1>')

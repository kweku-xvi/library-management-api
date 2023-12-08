import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('AUTH_TOKEN'))

def send_verification_email(email, username, link):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "HQRFKDHDK84B16GJAQ7PWPFATXS8",
            "data": {
            "username": username,
            "link": link,
            },
        }
    )


def send_password_reset_email(email, username, link):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "WF7909Y7ZWMNWNNTNNQRHDTBKDF4",
            "data": {
            "username": username,
            "link": link,
            },
        }
    )
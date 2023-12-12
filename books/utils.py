import os
from dotenv import load_dotenv
from trycourier import Courier

load_dotenv()

client = Courier(auth_token=os.getenv('AUTH_TOKEN'))

def send_checkout_book_email(email:str ,username:str, book:str, borrow_date:str, due_date:str):
    client.send_message(
        message={
            "to": {
            "email": email,
            },
            "template": "NT0WK2T7FVMSKDGA0W8YEQXE6GGZ",
            "data": {
            "username": username,
            "book": book,
            "borrow_date": borrow_date,
            "due_date": due_date,
            },
        }
    )

from json import load
import smtplib, ssl
import os
from dotenv import load_dotenv
load_dotenv()

def send(word):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("EMAIL")  # Enter your address
    receiver_email = os.getenv("MY_EMAIL")  # Enter receiver address
    password = os.getenv("PASSWORD")
    message = f"""\
    Subject: Today's Wordle

    Hi Jack,

    How are you today? You're looking great, as always.

    In case you were wondering, today's wordle is {word}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
# from twilio.rest import Client 
# from os import getenv as env
# from dotenv import load_dotenv
# from words import *
# load_dotenv()
 
# account_sid = env("ACCOUNT_SID")
# auth_token = env("AUTH_TOKEN")
# client = Client(account_sid, auth_token) 

def send(word):
    pass

# def send(word):
#     message = client.messages.create(body=f"FYI, today's wordle is... {word}", from_=env("OUTGOING_PHONE_NUMBER"), to=env("RECIPIENT_PHONE_NUMBER")) 

# if __name__ == "__main__":
#     send("test")
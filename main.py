import requests
import json
import time
import os
import openai

from datetime import datetime
from config import BOT_ID, ACCESS_TOKEN, OPENAI_KEY

openai.api_key = OPENAI_KEY
openai.organization = "org-LdSlWbJ9mw5Y4EqwxL2bRZaj"

# Function to send a message in the group using a pre-made bot
def send_msg(msg):
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": BOT_ID,
        "text": msg,
    }
    headers = {
        "Content-Type": "application/json"
    }

    send_txt = requests.post(url, json=data, headers=headers)

# Returns a list of the most recent 20 messages and their corresponding IDs
def update_msgs():
    # API call
    msgs = requests.get("https://api.groupme.com/v3/groups/95739422/messages?token=" + ACCESS_TOKEN)
    messages_texts = []
    # If call is a success, parse out the messages and IDs into a list
    if msgs.status_code == 200:
        data = msgs.json()
        messages = data["response"]["messages"]

        message_texts = []

        for message in messages:
            text = message.get("text")
            text_id = message.get("id")
            message_texts.append([text_id, text])
        
        return(message_texts)
    
    else:
        print("Failed API call")
        return(message_texts)


# This is the main loop. Every 3 seconds check for a new message. If it contains "Log: ", record the entry 
# into the "log.txt" file. Ignore all other messages
last_id = 0
while(True):
    # API call to get messages
    messages = update_msgs()

    if messages != None:
        if last_id != messages[0][0]:
            last_id = messages[0][0]
            parse_check = messages[0][1][0:5]
            if "log:" in parse_check.lower():
                # Get date of entry
                current_date = datetime.now()
                formatted_date = current_date.strftime("%d %b %Y %H:%M:%S")

                # Format full entry
                full_entry = formatted_date + ", " + messages[0][1][5:] + "\n"
                print("---- [NEW ENTRY] ----\n" + full_entry + "---------")
                
                # Append entry to local file
                with open("log.csv", "a+") as log_file:
                    log_file.write(full_entry)
                    log_file.seek(0)
                    past = log_file.readlines()
                
                # Send message in chat to confirm that the message was seen
                text_in = "given this:\n\n" + str(past[-20:]) + "\n\nmake a quick dissapointed and sarcastic comment about the following: " + messages[0][1][5:]
                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text_in}])
                send_msg(chat_completion.choices[0].message.content)   

    time.sleep(3)

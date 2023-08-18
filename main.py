import requests
import json
import time

from datetime import datetime
from config import BOT_ID, ACCESS_TOKEN

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


# This is the main loop. Every second check for a new message. If it contains "Log: ", record the entry 
# into the "log.txt" file. Ignore all other messages
last_id = 0
while(True):
    messages = update_msgs()

    if last_id != messages[0][0]:
        last_id = messages[0][0]
        if "log:" in messages[0][1].lower():
            # Get date of entry
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d %b %Y %H:%M:%S")

            # Format full entry
            full_entry = "Date: " + formatted_date + ", Entry: " + messages[0][1][5:] + "\n"
            print("---- [NEW ENTRY] ----\n" + full_entry + "---------")
            
            # Append entry to local file
            with open("log.txt", "a") as log_file:
                log_file.write(full_entry)
            
            # Send message in chat to confirm that the message was seen
            send_msg("Thank you, entry recorded")
    

    time.sleep(1)

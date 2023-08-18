import requests
import json
import time

from datetime import datetime
from config import BOT_ID, ACCESS_TOKEN

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

def update_msgs():
    msgs = requests.get("https://api.groupme.com/v3/groups/95739422/messages?token=" + ACCESS_TOKEN)
    # read_txt = requests.get(url, json=data, headers=headers)

    if msgs.status_code == 200:
        data = msgs.json()
        messages = data["response"]["messages"]

        message_texts = []

        for message in messages:
            text = message.get("text")
            text_id = message.get("id")
            message_texts.append([text_id, text])
        
        return(message_texts)

last_id = 0
while(True):
    messages = update_msgs()

    if last_id != messages[0][0]:
        last_id = messages[0][0]
        if "log:" in messages[0][1].lower():
            # Get date of entry
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d %b %Y %H:%M:%S")

            full_entry = "Date: " + formatted_date + ", Entry: " + messages[0][1][5:] + "\n"

            
            with open("log.txt", "a") as log_file:
                log_file.write(full_entry)

            send_msg("Thank you, entry recorded")
    

    time.sleep(1)

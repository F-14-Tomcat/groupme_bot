import requests
from config import BOT_ID, ACCESS_TOKEN

url = "https://api.groupme.com/v3/bots/post"
data = {
    "bot_id": BOT_ID,
    "text": "Another test from Wes",
    "attachments" : [
        {
        "type"  : "location",
        "lng"   : "40.000",
        "lat"   : "70.000",
        "name"  : "GroupMe HQ"
        }
    ]
}
headers = {
    "Content-Type": "application/json"
}

send_txt = requests.post(url, json=data, headers=headers)
# read_txt = requests.get(url, json=data, headers=headers)

print(read_txt)


# curl -X POST -d '{"bot_id": "4bc6f7816a4a4bbb8610be0e49", "text": "Hello world"}' -H 'Content-Type: application/json' https://api.groupme.com/v3/bots/post

# H-PACK
# curl -X POST -d '{"bot_id": "d183f3929f9920248ec68b2117", "text": "Hot indeed"}' -H 'Content-Type: application/json' https://api.groupme.com/v3/bots/post
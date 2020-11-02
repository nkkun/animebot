import requests
import json

BOT_TOKEN = ''
CHAT_ID = ''
MESSAGE_ID = '1523'


media = json.dumps({
    'type': 'photo',
    'media': 'https://www.writeups.org/wp-content/uploads/Ichigo-Kurosaki-Bleach-Shonen-Jump-c.jpg'
})

message = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageMedia?chat_id={CHAT_ID}&message_id={MESSAGE_ID}&media={media}"

result = requests.post(message)
print(result.json())

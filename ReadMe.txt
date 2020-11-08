
1. api.telegram.org/bot<token key>/getUpdates // updates on chat
2. api.telegram.org/bot<token key>/sendMessage?chat_id=<users unique id of chat>&text=<reply>
3. import telegram
4. bot = telegram.Bot('TOKEN') #firstly
5. bot.send_photo(get_chat_id(update),photo=url)
6. bot.send_video(get_chat_id(update), video) #video = 'url'

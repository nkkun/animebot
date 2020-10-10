import requests as requests
from bs4 import BeautifulSoup as soup
import validators
import os
from flask import Flask, request
import re

Token= "1382346231:AAFovu38e6OnV0qRqAg7wMmgmw9MZ6ImVUk"
url="https://api.telegram.org/bot1382346231:AAFovu38e6OnV0qRqAg7wMmgmw9MZ6ImVUk/"
server = Flask(__name__)
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id

def get_name(update):
    name = update['message']["from"]["first_name"]
    return name
    

def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


def last_update(req,offset=None):
    req= req + "getUpdates"
    if offset:
        req=req+"?offset={}".format(offset-10)
    response = requests.get(req)
    response = response.json()
    result=response["result"]
    total_updates=len(result)-1
    return result[total_updates]

def sender(url,update):
    login={'_csrf': 0,
    'email': 'ransomsumit@aol.com',
    'password': 'Beluga#44'}

    with requests.Session() as s:
        url1 = "https://gogoanime.so/login.html"
        r = s.get(url1 , headers={'User-Agent': 'Mozilla/5.0'})
        soupy = soup(r.content, 'html.parser')
        t = soupy.find('meta' , attrs={'name':"csrf-token"})['content']
        login['_csrf']=t
        r = s.post(url1, data = login, headers={'User-Agent': 'Mozilla/5.0'})
        r= r.text
        req = s.get(url , headers={'User-Agent': 'Mozilla/5.0'})
        page_soup = soup(req.content, "html.parser")
        title = page_soup.find_all('div', class_='cf-download')
        if(len(title)>0):
            title=title[0].find_all('a')
    
            for i in range(len(title)):
                title[i]=title[i].attrs['href']
                send_message(get_chat_id(update),str(i+1))
                send_message(get_chat_id(update),str(title[i]))
        else:
            send_message(get_chat_id(update),"wrongly written or Not available check again")

def send_message(chat_id,message_text):
    params = {"chat_id":chat_id,"text":message_text}
    response = requests.post(url + "sendMessage",data=params)
    return response

def main():
    update_id = last_update(url)["update_id"]
    update_id = last_update(url,update_id)["update_id"]
    while True:
        update = last_update(url)
        if (update_id == update["update_id"]):
            if (get_message_text(update).lower()=="hi" or get_message_text(update).lower()=="hello" or get_message_text(update).lower()=="henlo"):
                send_message(get_chat_id(update),"Hello, " + get_name(update) + " type /search to start searching")
                update_id = last_update(url,update_id)["update_id"]
                update_id=update_id+1
            elif (get_message_text(update).lower()[:7]=="/search"):
                if(get_message_text(update).lower()=='/search'):
                    send_message(get_chat_id(update),"enter search keyword and wait until it finishes the search with downloading instructions:")
                else:
                    surl2= 'https://gogoanime.so//search.html?keyword='+str("%20".join(get_message_text(update)[7:].lower().split()))
                    r = requests.get(surl2 , headers={'User-Agent': 'Mozilla/5.0'})
                    page_soup = soup(r.content, "html.parser")
                    title = page_soup.find_all('p', class_='name')
                    for i in range(len(title)):
                        title[i]=title[i].find('a')
                 
                    for tit in title:
                        link = tit.attrs['title']
                        send_message(get_chat_id(update),str(link))
                send_message(get_chat_id(update),'copy the name of the anime you want, write "/link "+ paste the name + add the episode no. as "episode 1" <--> for example "/link one piece episode 1"')
    
                update_id = last_update(url,update_id)["update_id"]
                update_id = update_id+1

                
            elif (get_message_text(update).lower()=="/updates"):
                surl4= 'https://gogoanime.so'
                r = requests.get(surl4 , headers={'User-Agent': 'Mozilla/5.0'})
                souper=soup(r.content, "html.parser")
                tit = souper.find_all('p', class_='name')
                for i in range(len(tit)):
                    tit[i]=tit[i].find('a')
                for l in range(len(tit)):
                    tit[l]=tit[l].attrs['href'][1:]
                    send_message(get_chat_id(update),str(tit[l]))
                send_message(get_chat_id(update),'copy the name of the anime you want, write "/link "+ paste the name + add the episode no. as "episode 1"')
                send_message(get_chat_id(update),'for example "/link one piece episode 1"')
                update_id = last_update(url,update_id)["update_id"]
                update_id=update_id+1
                
            elif (get_message_text(update).lower()=="/start"):
                send_message(get_chat_id(update),"say hi")
                update_id=update_id+1
            elif (get_message_text(update).lower()[0:5]=="/link"):
                s=get_message_text(update).lower()[6:]
                a=""
                for k in s.split("/n"):
                    a=a+(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
                update_id=update_id+1
                surl3= 'https://gogoanime.so/' + str('-'.join(a.split()))
                if(validators.url(surl3)==True):
                    sender(surl3,update)
                else:
                    send_message(get_chat_id(update),"wrongly written or Not available check again")
                    
            else:
                 surl2= 'https://gogoanime.so//search.html?keyword='+str("%20".join(get_message_text(update).lower().split()))
                 r = requests.get(surl2 , headers={'User-Agent': 'Mozilla/5.0'})
                 page_soup = soup(r.content, "html.parser")
                 title = page_soup.find_all('p', class_='name')
                 for i in range(len(title)):
                     title[i]=title[i].find('a')
                 
                 for tit in title:
                     link = tit.attrs['title']
                     send_message(get_chat_id(update),str(link))
                 send_message(get_chat_id(update),'copy the name of the anime you want, write "/link "+ paste the name + add the episode no. as "episode 1" <--> for example "/link one piece episode 1"')
                 update_id = last_update(url,update_id)["update_id"]
                 update_id=update_id+1

main()

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://stark-thicket-09976.herokuapp.com/ ' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))



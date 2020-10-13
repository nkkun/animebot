import requests as requests
from bs4 import BeautifulSoup as soup
import validators
import os
from flask import Flask, request
import re
import telepot

Token= "1382346231:AAFovu38e6OnV0qRqAg7wMmgmw9MZ6ImVUk"
bot = telepot.Bot(Token)
url="https://api.telegram.org/bot1382346231:AAFovu38e6OnV0qRqAg7wMmgmw9MZ6ImVUk/"
server = Flask(__name__)
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id

def get_name(update):
    name = update['message']["from"]["first_name"]
    return name
    

def get_message_text(update):
    if("message" in update.keys()):
        if('text' in update['message'].keys()):
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

def about(txt,update):
    a=""
    for k in txt.split("/n"):
        a=a+(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
        surl5= 'https://gogoanime.so/category/' + str('-'.join(a.split()))
        if(validators.url(surl5)==True):
            r = requests.get(surl5, headers={'User-Agent': 'Mozilla/5.0'})
            so = soup(r.content, 'html.parser')
            abo = so.find_all('p', class_='type')
            if(len(abo)>0):
                abo[0]=str(abo[0].find('span').getText()) + str(abo[0].find('a').attrs['title'])
                abo[1]= str(abo[1].getText())
                x=abo[2].find_all('a')
                s=""
                for i in range(len(x)):
                    s+=x[i].getText()
                abo[2]= str(abo[2].find('span').getText()) + s
                s=""
                abo[3]= str(abo[3].getText())
                abo[4]= str(abo[4].getText())
                abo[5]= str(abo[5].getText())
                img=so.find('div', class_='anime_info_body')
                img=img.find('img')
                img=img.attrs['src']
                bot.sendPhoto(get_chat_id(update), img)
                abo.append("Episodes: "+ str(so.find('a', class_='active').getText()))
                for i in range(len(abo)):
                    s=s+abo[i]+'\n' + '\n'
                send_message(get_chat_id(update),s)
            else:
                send_message(get_chat_id(update),'Oni Chan! it appears that you have typed the name wrong or the link is broken :(')
        else:
             send_message(get_chat_id(update),'Oni Chan! it appears that you have typed the name wrong or the link is broken :(')

#def batch(txt,update):
    
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
                send_message(get_chat_id(update),str(title[i]))
        else:
            send_message(get_chat_id(update),("wrongly written or Not available, Possible solutions \n \n" +
                                              "Search for the anime name and paste it as it is written \n \n" +
                                              "remember 'episode' should be written completely, no short cuts like 'ep' \n \n" +
                                              "episode number doesn't exist check by writing /about"))
            

def send_message(chat_id,message_text):
    params = {"chat_id":chat_id,"text":message_text}
    response = requests.post(url + "sendMessage",data=params)
    return response

def main():
    update_id = last_update(url)["update_id"]
    update_id = last_update(url,update_id)["update_id"]
    while True:
        update = last_update(url)
        if(get_message_text(update)):
            if (update_id == update["update_id"]):
                if (get_message_text(update).lower()=="/start"):
                    send_message(get_chat_id(update),"Hi, I am here to help you find anime")
                    update_id=update_id+1

                
                elif (get_message_text(update).lower()[:7]=="/search"):
                    if((get_message_text(update).lower()=='/search') or ((get_message_text(update).lower()[:7]=='/search')
                                                                         and (get_message_text(update)[-13:]=='@Any_Animebot'))):
                        send_message(get_chat_id(update),"/search <enter short name of the anime>")
                    else:
                        surl2= 'https://gogoanime.so//search.html?keyword='+str("%20".join(get_message_text(update)[7:].lower().split()))
                        r = requests.get(surl2 , headers={'User-Agent': 'Mozilla/5.0'})
                        page_soup = soup(r.content, "html.parser")
                        title = page_soup.find_all('p', class_='name')
                        for i in range(len(title)):
                            title[i]=title[i].find('a')
                        s=""
                        for tit in title:
                            link = tit.attrs['title']
                            s=s+str(link)+"\n \n"
                        send_message(get_chat_id(update),s)
                        send_message(get_chat_id(update),'copy the name of the anime you want, write "/link "+ paste the name + add the episode no. as "episode 1" \n for example "/link one piece episode 1"')
                    update_id = last_update(url,update_id)["update_id"]
                    update_id = update_id+1
                
                elif (get_message_text(update).lower()[:6]=="/about"):
                    if((get_message_text(update).lower()=='/about') or ((get_message_text(update).lower()[:6]=='/about')
                                                                         and (get_message_text(update)[-13:]=='@Any_Animebot'))):
                        send_message(get_chat_id(update),"/about <enter name as it was found in the search>")
                        update_id = last_update(url,update_id)["update_id"]
                        update_id = update_id+1
                    else:
                        about(get_message_text(update).lower()[6:],update)
                        update_id = last_update(url,update_id)["update_id"]
                        update_id = update_id+1
                    
                    
                elif ((get_message_text(update).lower()=="/help") or ((get_message_text(update).lower()[:5]=='/help')
                                                                         and (get_message_text(update)[-13:]=='@Any_Animebot'))):
                    send_message(get_chat_id(update),('/link < add anime name from search with episode "number" > \n' +
                                                      'for example "/link one piece episode 1" \n \n' + '/search < small anime tag such as "shippuden" > \n \n' +
                                                      '/updates "get you the latest anime releases" \n \n' + "/about <enter name as it was found in the search>"))
                    update_id = last_update(url,update_id)["update_id"]
                    update_id=update_id+1
                

                elif ((get_message_text(update).lower()=="/updates") or ((get_message_text(update).lower()[:8]=='/updates')
                                                                         and (get_message_text(update)[-13:]=='@Any_Animebot'))):
                    surl4= 'https://gogoanime.so'
                    r = requests.get(surl4 , headers={'User-Agent': 'Mozilla/5.0'})
                    souper=soup(r.content, "html.parser")
                    tit = souper.find_all('p', class_='name')
                    for i in range(len(tit)):
                        tit[i]=tit[i].find('a')
                    s=""
                    for l in range(len(tit)):
                        tit[l]=tit[l].attrs['href'][1:]
                        s=s+str(tit[l]) + "\n \n"
                    send_message(get_chat_id(update),s)
                    send_message(get_chat_id(update),('copy the name of the anime you want, write "/link" + paste the name + add the episode no. as "episode 1" \n \n' +
                                                      'for example "/link one piece episode 1"'))
                    update_id = last_update(url,update_id)["update_id"]
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
                        send_message(get_chat_id(update),"wrongly written or Not available check again \n format: /link one piece episode 1")
                else:
                    update_id = last_update(url,update_id)["update_id"]
                    update_id = update_id+1
                    
                '''elif(get_message_text(update).lower()[0:6]=="/batch"):
                     if(get_message_text(update).lower()=='/batch'):
                        send_message(get_chat_id(update),"/batch <episode range like '10-20'> <enter name as it was found in the search>")
                        update_id = last_update(url,update_id)["update_id"]
                        update_id = update_id+1'''
                
        else:
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



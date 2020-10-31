import os
import re
import sys
import time
import telepot
import validators
import requests as requests
from flask import Flask, request
from bs4 import BeautifulSoup as soup
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from telepot.delegate import pave_event_space, per_chat_id, create_open, \
    include_callback_query_chat_id, per_inline_from_id


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    group_id=chat_id

    if content_type == 'text':
        if msg['text'][:7] == '/search':
            chat_id= msg['from']['id']
            if((msg['text'].lower()=='/search') or ((msg['text'].lower()[:7]=='/search')
                                                                   and (msg['text'][-14:]==' @Any_Animebot'))):
                if(group_id==chat_id):
                    bot.sendMessage(chat_id,"/search 'enter short name of the anime and wait for our personal message in your Inbox'")
                else:
                    bot.sendMessage(group_id,"/search 'enter short name of the anime and wait for our personal message in your Inbox'")
                        
            elif(msg['text'][:20]=='/search@Any_Animebot'):
                bot.sendMessage(group_id,"/search 'enter short name of the anime without the bot name'")
            else:
                s=msg['text'][8:]
                s = re.sub('\W+',' ', s)
                surl2= 'https://gogoanime.so//search.html?keyword='+str("%20".join(s.lower().split()))
                r = requests.get(surl2 , headers={'User-Agent': 'Mozilla/5.0'})
                page_soup = soup(r.content, "html.parser")
                title = page_soup.find_all('p', class_='name')
                lob=[]
                for i in range(len(title)):
                    title[i]=title[i].find('a')
                inl= []
                for tit in title:
                    link = tit.attrs['title']
                    lob=tit.attrs['href']
                    if(len(link)>50):
                        inl.append([InlineKeyboardButton(text=str(link)[:18] + "....."+ str(link)[-18:], url="https://gogoanime.so/"+str(lob)[10:]+"-episode-1")])
                    else:
                        inl.append([InlineKeyboardButton(text=str(link), parse_mode='Markdown', callback_data=str(lob)[10:]+"about")])

                bot.sendMessage('1152801694',msg['text'] +" "+ msg['from']['first_name'])
                if(group_id==chat_id):
                    bot.sendMessage(chat_id,"RESULTS",reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
                else:
                    bot.sendMessage(group_id,"/search <check for our personal message in your Inbox>")
                    bot.sendMessage(chat_id,"RESULTS",reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
    if content_type == 'text':
        if msg['text'][:5] == '/help':
            if((msg['text'].lower()=='/help') or ((msg['text'].lower()[:5]=='/help')
                                                                     and (msg['text'][-13:]=='@Any_Animebot'))):
                bot.sendMessage(chat_id,"Just type /search plus the name of the anime with a space, we will send you a Personal Message soon if something doesn't work contact @Ransom_s")

    if content_type == 'text':
        if msg['text'][:8] == '/updates':
            if((msg['text'].lower()=='/updates') or ((msg['text'].lower()[:8]=='/updates')
                                                                     and (msg['text'][-13:]=='@Any_Animebot'))):
                surl4= 'https://gogoanime.so/'
                r = requests.get(surl4 , headers={'User-Agent': 'Mozilla/5.0'})
                souper=soup(r.content, "html.parser")
                tit = souper.find_all('p', class_='name')
                for i in range(len(tit)):
                    tit[i]=tit[i].find('a')
                for l in range(len(tit)):
                    tit[l]=tit[l].attrs['href'][1:]
                inl=[]
                urlu=[]
                for it in tit:
                    cou=0
                    ep=""
                    for i in range(-1,-20,-1):
                        if(cou<1 and it[i]=="-"):
                            cou+=1
                            ep=it[i+1:]
                        elif(cou==1 and it[i]=="-"):
                            cou+=1
                            it=it[:i]
                            
                    if(len(it)>50):
                        inl.append([InlineKeyboardButton(text=str(it)[:18] + "....."+ str(it)[-18:] + " Ep " + ep, url="https://gogoanime.so/" + it +"-episode-"+ep)])
                        urlu.append([InlineKeyboardButton(text=str(it)[:18] + "....."+ str(it)[-18:] + " Ep " + ep, url="https://gogoanime.so/" + it)])
                    else:
                        inl.append([InlineKeyboardButton(text=str(it) + " Ep "+ep, parse_mode='Markdown', callback_data=str(it)+"/"+ep+"link")])
                        urlu.append([InlineKeyboardButton(text=str(it) + " Ep " + ep,url="https://gogoanime.so/" + it +"-episode-"+ep)])
                if(msg['from']['id']==chat_id):
                    bot.sendMessage(msg['from']['id'],"Latest Updates in anime world",reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
                else:
                    bot.sendMessage(msg['from']['id'],"Latest Updates in anime world",reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
                    bot.sendMessage(chat_id,"Latest Updates in anime world",reply_markup = InlineKeyboardMarkup(inline_keyboard=urlu))
        
                            
def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')

    if(msg['message']['chat']['type']=='group'):
        chat_id=msg['message']['chat']['id']
    ide=(chat_id,msg['message']['message_id'])
    if (query_data[-5:]=="about"):
        bot.editMessageReplyMarkup(ide, reply_markup=None)
        a=""
        for k in query_data[:-5].split("/n"):
            #a=a+(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
            surl5= 'https://gogoanime.so/category/' + str(k) #str('-'.join(a.split()))
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
                    abo.append("Episodes: "+ str(so.find('a', class_='active').getText()))
                    for i in range(len(abo)):
                        s=s+abo[i]+'\n' + '\n'
                    bot.sendPhoto(chat_id, img)
                    bot.sendMessage(chat_id,s)
                    inl= []
                    oof= "https://gogoanime.so/" +query_data[:-5] + "-episode-1"
                    if(len(str(query_data[:-5])+ " episode")>64):
                        bot.sendMessage(chat_id, "error occured due to long name, try website")
                        inl.append([InlineKeyboardButton(text="Download", url=oof)])
                        inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data="searchback")])
                    else:
                        inl.append([InlineKeyboardButton(text="Download", parse_mode='Markdown', callback_data=str(query_data[:-5])+ " episode")])
                        inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data="searchback")])
                    bot.sendMessage(chat_id, "Choose your episode from the list" ,reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
    
                else:
                    bot.sendMessage(chat_id, "error occured")
                        
    elif (query_data[-7:]=="episode"):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        if(msg['message']['chat']['type']=='group'):
            chat_id=msg['message']['chat']['id']
        ide=(chat_id,msg['message']['message_id'])
        for k in query_data[:-8].split("/n"):
            #a=a+(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
            surl5= 'https://gogoanime.so/category/' + str(k) #str('-'.join(a.split()))
            if(validators.url(surl5)==True):
                r = requests.get(surl5, headers={'User-Agent': 'Mozilla/5.0'})
                so = soup(r.content, 'html.parser')
                abo = so.find('a', class_='active')
                abo=abo.attrs['ep_end']
                inl=[]
                if(int(abo)<=28):
                    temp=[]
                    for i in range(1,int(abo)+1):
                        if(i%7==0):
                            temp.append(InlineKeyboardButton(text="Ep" + str(i), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(i)+"link"))
                            inl.append(temp)
                            temp=[]
                        else:
                            temp.append(InlineKeyboardButton(text="Ep" + str(i), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(i)+"link"))
                            if(i==int(abo)):
                                inl.append(temp)
                    bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                elif(int(abo)//28==1):
                    temp=[]
                    for i in range(1,26):
                        if(i%7==0):
                            temp.append(InlineKeyboardButton(text="Ep" + str(i), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(i)+"link"))
                            inl.append(temp)
                            temp=[]
                        else:
                            temp.append(InlineKeyboardButton(text="Ep" + str(i), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(i)+"link"))
                            if(i==25):
                                inl.append(temp)
                    inl[3].append(InlineKeyboardButton(text="Ep26-" + str(abo), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+"26-"+str(abo)+"/"))
                    bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                    
                else:
                    temp=[]
                    rem=int(abo)//16
                    for i in range(1,16):
                        low=rem*i-(rem-1)
                        high=rem*i
                        if(i%4==0):
                            temp.append(InlineKeyboardButton(text = "Ep" + str(low) + "-" + str(high), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(low)+"-"+str(high)+"/"))
                            inl.append(temp)
                            temp=[]
                        else:
                            temp.append(InlineKeyboardButton(text = "Ep" + str(low) + "-" + str(high), parse_mode='Markdown', callback_data=str(query_data[:-8])+ "/"+str(low)+"-"+str(high)+"/"))
                            if(i==15):
                                inl.append(temp)
                    inl[3].append(InlineKeyboardButton(text="Ep" + str(rem*15 + 1) + "-" + str(abo), parse_mode='Markdown', callback_data=str(query_data[:-8])
                                                       + "/"+ str(rem*15 + 1) + "-" +str(abo)+"/"))
                    bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                    
                #bot.sendMessage(chat_id, "Choose Your Episode" ,reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))
    elif (query_data[-1]=="/"):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        if(msg['message']['chat']['type']=='group'):
            chat_id=msg['message']['chat']['id']
        ide=(chat_id,msg['message']['message_id'])
        low=high=pos=0
        q=""
        for i in range(-2,-10,-1):
            if(query_data[i]=="/"):
                pos=i
        s=query_data[pos+1:-1]
        for i in s:
            if(i=="-"):
                low=int(q)
                q=""
            else:
                q=q+i
        high=int(q)
        inl=[]
            
        if(high-low+1<=16):
            temp=[]
            for i in range(1,high-low+2):
                if(i%4==0):
                    temp.append(InlineKeyboardButton(text="Ep" + str(low-1+i), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(low-1+i)+"link"))
                    inl.append(temp)
                    temp=[]
                else:
                    temp.append(InlineKeyboardButton(text="Ep" + str(low-1+i), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(low-1+i)+"link"))
            inl.append(temp)
            inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data=query_data[:pos]+" episode")])
            bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                    
                    
        elif((high-low+1)//16==1):
            temp=[]
            for i in range(1,16):
                if(i%4==0):
                    temp.append(InlineKeyboardButton(text="Ep" + str(low-1+i), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(low-1+i)+"link"))
                    inl.append(temp)
                    temp=[]
                else:
                    temp.append(InlineKeyboardButton(text="Ep" + str(low-1+i), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(low-1+i)+"link"))
                    if(i==15):
                        inl.append(temp)
            inl[3].append(InlineKeyboardButton(text="Ep" + str(low+15) + "-" + str(high), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/" + str(low+15) + "-" + str(high)+"/"))
            inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data=query_data[:pos]+" episode")])
            bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                
        else:
            temp=[]
            rem=(high-low+1)//16
            slow=shigh=0
            for i in range(1,16):
                slow=low+rem*i-(rem-1)-1
                shigh=low+rem*i-1
                if(i%4==0):
                    temp.append(InlineKeyboardButton(text = "Ep" + str(slow) + "-" + str(shigh), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(slow)+"-"+str(shigh)+"/"))
                    inl.append(temp)
                    temp=[]
                else:
                    temp.append(InlineKeyboardButton(text = "Ep" + str(slow) + "-" + str(shigh), parse_mode='Markdown', callback_data=str(query_data[:pos])+ "/"+str(slow)+"-"+str(shigh)+"/"))
                    if(i==15):
                        inl.append(temp)
            inl[3].append(InlineKeyboardButton(text="Ep" + str(low+rem*15) + "-" + str(high), parse_mode='Markdown', callback_data=str(query_data[:pos])
                                                       + "/"+ str(low+rem*15) + "-" +str(high)+"/"))
            inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data=query_data[:pos]+" episode")])
            bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
                
    elif (query_data[-4:]=="link"):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        
        if(msg['message']['chat']['type']=='group'):
            chat_id=msg['message']['chat']['id']
        ide=(chat_id,msg['message']['message_id'])
        pos=0
        num=""
        for i in range(-5,-10,-1):
            if(query_data[i]=="/"):
                pos=i
                break
            else:
                num=num+query_data[i]
        num=(num[::-1])
        url= 'https://gogoanime.so/' + query_data[:pos] + "-episode-" + num
        inl=[]
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
                    tex=title[i].getText()
                    title[i]=title[i].attrs['href']
                    inl.append([InlineKeyboardButton(text="Ep "+num+" "+ tex, url=title[i])])
            inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data=query_data[:pos]+" episode")])
            bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))

    elif (query_data=="searchback"):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        if(msg['message']['chat']['type']=='group'):
            chat_id=msg['message']['chat']['id']
        ide=(chat_id,msg['message']['message_id'])
        bot.answerCallbackQuery(query_id, text="Search Again", show_alert = True)
            
        
    '''def on_inline_query(self, msg):
        def compute():
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            self._count += 1
            text = '%d. %s' % (self._count, query_string)

            articles = [InlineQueryResultArticle(
                            id='abc',
                            title=text,
                            input_message_content=InputTextMessageContent(
                                message_text=text
                            )
                       )]

            return articles

        self.answerer.answer(msg, compute)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)'''

TOKEN= "1382346231:AAFovu38e6OnV0qRqAg7wMmgmw9MZ6ImVUk"

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)


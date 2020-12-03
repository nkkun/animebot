import requests
import re
import os
import json
import random
import telepot
import pyshorteners
from bs4 import BeautifulSoup as soup
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


q = pyshorteners.Shortener()
TOKEN = os.environ.get("bot_api")
bot = telepot.Bot(TOKEN)

def image_update(group_id, msg_id, url):
  media = json.dumps({'type': 'photo', 'media': url})
  message = f"https://api.telegram.org/bot{TOKEN}/editMessageMedia?chat_id={group_id}&message_id={msg_id}&media={media}"
  result = requests.post(message)


def hen_about(name, url, group_id, ide, msg):
  req = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  details = so.find('div', class_ = "su-row")
  img = details.find("img").attrs['src']
  details = details.find_all("div", class_ = "su-column-inner su-u-clearfix su-u-trim")
  details = "Name: " + name + "\n\n" + details[1].getText().strip()[:900] + "\n\nType '/hentai <name of hentai> to get search results."
  result = so.find_all("div", class_ = "su-button-center")
  temp = []
  for i in range(len(result)):
    result[i] = result[i].find("a")
    if "rel" in result[i].attrs:
      continue
    else:
      temp.append(result[i].attrs['href'])
  inl=[]
  temp1=[]
  if ide == 0:
    if len(url)>40:
      for i in range(1, len(temp)+1):
        if i % 7 == 0:
            url = temp[i-1]
            url = q.chilpit.short(url)
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
            inl.append(temp1)
            temp1 = []
        else:
            url = temp[i-1]
            url = q.chilpit.short(url)
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
            if i == len(temp):
                inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      bot.sendPhoto(group_id, img, caption = details, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
    else:
      for i in range(1, len(temp)+1):
        if i % 7 == 0:
          url = temp[i-1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i-1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if i == len(temp):
              inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      bot.sendPhoto(group_id, img, caption = details, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
  else:
    if len(url)>40:
      for i in range(1, len(temp)+1):
        if i % 7 == 0:
            url = temp[i-1]
            url = q.chilpit.short(url)
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
            inl.append(temp1)
            temp1 = []
        else:
            url = temp[i-1]
            url = q.chilpit.short(url)
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
            if i == len(temp):
                inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      image_update(group_id, msg['message']['message_id'], img)
      bot.editMessageCaption(ide, caption = details)
      bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
    else:
      for i in range(1, len(temp)+1):
        if i % 7 == 0:
          url = temp[i-1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i-1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if i == len(temp):
              inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      image_update(group_id, msg['message']['message_id'], img)
      bot.editMessageCaption(ide, caption=details)
      bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))

def hen_about1(name, url, group_id, ide, msg):
  req = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  img = so.find("div", class_ = "one_half")
  img = img.find("img").attrs['src']
  details = so.find("div", class_ = "one_half column-last")
  details = details.getText().strip()
  temp = so.find_all("div", class_ = "tab_content clearfix")
  for i in range(len(temp)):
    temp[i] = temp[i].find("a").attrs['href']
  details = "Name: " + name + "\n\n" + details[:900] + "\n\nType '/hentai <name of hentai> to get search results."
  temp1=[]
  inl=[]
  if ide == 0:
    if (len(url)>40):
      for i in range(1, len(temp)+1):
        if (i % 7 == 0):
          url = temp[i-1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i-1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if (i == int(len(temp))):
              inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      bot.sendPhoto(group_id, img, caption = details, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
    else:
      for i in range(1, len(temp)+1):
        if (i % 7 == 0):
            url = temp[i-1]
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
            inl.append(temp1)
            temp1 = []
        else:
            url = temp[i-1]
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
            if (i == int(len(temp))):
                inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      bot.sendPhoto(group_id, img, caption = details, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
  else:
    if (len(url)>40):
      for i in range(1, len(temp)+1):
        if (i % 7 == 0):
          url = temp[i-1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i-1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if (i == int(len(temp))):
              inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      image_update(group_id, msg['message']['message_id'], img)
      bot.editMessageCaption(ide, caption=details)
      bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
    else:
      for i in range(1, len(temp)+1):
        if i % 7 == 0:
            url = temp[i-1]
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url+"~link"))
            inl.append(temp1)
            temp1 = []
        else:
            url = temp[i-1]
            temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
            if i == int(len(temp)):
                inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown',callback_data= "random")])
      image_update(group_id, msg['message']['message_id'], img)
      bot.editMessageCaption(ide, caption=details)
      bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))

  
def hen_search(group_id, st):
  req = requests.get("http://www.xanimeporn.com/hentai-list/", headers = {"User-Agent" : "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  result = so.find_all("td", style = "text-align:left")
  temp ={}
  for i in range(len(result)):
    result[i] = result[i].find("a")
    temp[result[i].getText()] = result[i].attrs['href']
  st = re.sub('\W+','',st.strip())
  res = {}
  for i in temp.keys():
    x = re.sub('\W+', '', i.strip()).lower()
    if st.lower() in x:
      res[i] = temp[i]
  inl=[]
  for i in res.keys():
    if(len(inl) == 10):
      break
    if(len(res[i])>40):
      url = q.chilpit.short(res[i])
      inl.append([InlineKeyboardButton(text=i, parse_mode='Markdown',callback_data= url + "~about")])
    else:
      inl.append([InlineKeyboardButton(text=i, parse_mode='Markdown', callback_data=res[i] + "~about")])
  if len(res) > 10:
      bot.sendMessage(group_id, text= "Results, truncated with 10 results", reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
  elif len(res) == 0:
    bot.sendMessage(group_id, text="OwO, Nothing Found")
  else:
    bot.sendMessage(group_id, text="Results", reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
  

def hen_rand(group_id, msg, ide):
  req = requests.get("http://www.xanimeporn.com/hentai-list/", headers = {"User-Agent" : "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  result = so.find_all("td", style = "text-align:left")
  temp ={}
  for i in range(len(result)):
    result[i] = result[i].find("a")
    temp[result[i].getText()] = result[i].attrs['href']
  choice = list(temp.keys())
  r = random.choice(choice)
  print(r)
  try:
    hen_about(r, temp[r], group_id, ide, msg)
  except Exception as e:
    try:
      hen_about1(r, temp[r], group_id, ide, msg)
    except Exception as j:
      print(j)
      bot.sendMessage(group_id, "Error occured try again", reply_to_message_id=msg['message_id'])


def hen_links(url, ide):
  if(url.find("chilp")!= -1):
    url = q.chilpit.expand(url)
  req = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  links = so.find_all("div", class_ = "su-button-center")
  temp = []
  for i in range(len(links)):
    links[i] = links[i].find("a")
    if "rel" in links[i].attrs:
      temp.append(links[i].attrs['href'])
  pos = url.find("-episode")
  back_url = url[:pos]
  if(len(back_url)> 40):
    back_url = q.chilpit.short(back_url)
  pos = url.find("-sub")
  num = url[pos-1]
  inl=[]
  for i in range(len(temp)):
    inl.append([InlineKeyboardButton(text="Ep " + num + " " + temp[i][-4:], url=temp[i])])
  inl.append([InlineKeyboardButton(text="Back", parse_mode='Markdown', callback_data=back_url + "~back")])
  bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))

def hen_back(url, ide):
  if(url.find("chilp") != -1):
    url = q.chilpit.expand(url)
  req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  result = so.find_all("div", class_="su-button-center")
  temp = []
  for i in range(len(result)):
    result[i] = result[i].find("a")
    if "rel" in result[i].attrs:
      continue
    else:
      temp.append(result[i].attrs['href'])
  if len(temp) == 0:
    hen_back1(url, ide)
  else:
    inl = []
    temp1 = []
    if len(url) > 40:
      for i in range(1, len(temp) + 1):
        if i % 7 == 0:
          url = temp[i - 1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i - 1]
          url = q.chilpit.short(url)
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if i == len(temp):
            inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown', callback_data="random")])
      bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
    else:
      for i in range(1, len(temp) + 1):
        if i % 7 == 0:
          url = temp[i - 1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          inl.append(temp1)
          temp1 = []
        else:
          url = temp[i - 1]
          temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
          if i == len(temp):
            inl.append(temp1)
      inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown', callback_data="random")])
      bot.editMessageReplyMarkup(ide, reply_markup = InlineKeyboardMarkup(inline_keyboard=inl))

def hen_back1(url, ide):
  if (url.find("chilp") != -1):
    url = q.chilpit.expand(url)
  req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
  so = soup(req.content, "html.parser")
  temp = so.find_all("div", class_="tab_content clearfix")
  for i in range(len(temp)):
    temp[i] = temp[i].find("a").attrs['href']
  temp1 = []
  inl = []
  if len(url) > 40:
    for i in range(1, len(temp) + 1):
      if i % 7 == 0:
        url = temp[i - 1]
        url = q.chilpit.short(url)
        temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
        inl.append(temp1)
        temp1 = []
      else:
        url = temp[i - 1]
        url = q.chilpit.short(url)
        temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
        if (i == int(len(temp))):
          inl.append(temp1)
    inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown', callback_data="random")])
    bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
  else:
    for i in range(1, len(temp) + 1):
      if i % 7 == 0:
        url = temp[i - 1]
        temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
        inl.append(temp1)
        temp1 = []
      else:
        url = temp[i - 1]
        temp1.append(InlineKeyboardButton(text=str(i), parse_mode='Markdown', callback_data=url + "~link"))
        if i == int(len(temp)):
          inl.append(temp1)
    inl.append([InlineKeyboardButton(text="RANDOM!!", parse_mode='Markdown', callback_data="random")])
    bot.editMessageReplyMarkup(ide, reply_markup=InlineKeyboardMarkup(inline_keyboard=inl))
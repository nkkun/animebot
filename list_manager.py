import re
lst={}
def adder(chat_id, name):
    lst[chat_id] = name
def list_search(x, chat_id):
    m = re.sub(r'[^\w]', ' ', lst[chat_id].lower())
    if(x == ""):
        return False
    else:
        x = re.sub(r'[^\w]', ' ', x)
        x = x.strip().split()
        flag = 0
        if(len(x)==0):
            return False
        else:
            for i in x:
                if i in m.split():
                    flag = 0
                else:
                    flag = 1
        if flag == 1:
            return False
        else:
            return True
def purge(chat_id):
    del lst[chat_id]

def check(chat_id):
    if chat_id in lst.keys():
        return True
    else:
        return False
def ret(chat_id):
    return lst[chat_id]
 

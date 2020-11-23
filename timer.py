from datetime import datetime
time_check={}

def tcheck(chat_id):
    if (chat_id in time_check.keys()):
        return True
    else:
        return False

def save(chat_id, t):
    time_check[chat_id] = t

def ttime(t,chat_id):
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(t, FMT) - datetime.strptime(time_check[chat_id], FMT)
    if(tdelta.total_seconds()<=120):
        return True
    else:
        return False

def time_purge(chat_id):
    del time_check[chat_id]


lst={}
def adder(chat_id, name):
    lst[chat_id] = name
    print(lst[chat_id])
def list_search(x, chat_id):
    if(x == ""):
        return False
    else:
        x = x.strip().split()
        flag = 0
        for i in x:
            if i in lst[chat_id].split():
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
 

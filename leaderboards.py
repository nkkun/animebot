import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
creds_dict = json.loads(json_creds)
creds_dict['private_key'] = creds_dict['private_key'].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1IvaiqN7D0GJqS6t9Bhq2vScfk1phH6EHh_mrhah4rk0/edit#gid=0")
sheet = spreadsheet.sheet1

def top_leaders(chat_id):
    temp = {}
    data = sheet.get_all_values()
    for i in range(len(data)):
        temp[data[i][0]] = int(data[i][2])
    temp = dict(sorted(temp.items(), key=lambda item: item[1], reverse=True))
    count = 0
    leaders = ""
    for i in temp.keys():
        count += 1
        if count == 11:
            break
        else:
            row_no = sheet.find(i).row
            data = sheet.row_values(row_no)
            data = '<a href="tg://user?id='+ str(data[0]) + '">' + data[1] + "</a>"
            leaders = leaders + str(count) + ". " + data + " -- " + str(temp[i]) + "\n"

    if chat_id in list(temp.keys()):
        rank = leaders + "\nYour rank is: " + str(list(temp.keys()).index(chat_id) + 1) \
               + " with score " + str(temp[chat_id])
    else:
        rank = "<b>" + leaders + "\nYour Score is 0" + "</b>"
    return rank


def purge_row(row_no):
    row1 = row_no[0].row
    cell1 = "C" + str(row1) 
    for i in range(1,len(row_no)):
        r = row_no[i].row
        cell = "C" + str(r)
        score1 = int(sheet.acell(cell1, value_render_option='FORMATTED_VALUE').value)
        score = int(sheet.acell(cell, value_render_option='FORMATTED_VALUE').value)
        sheet.update_acell(cell1, score1+score)
        sheet.update_acell("A" + str(r), "")
        sheet.update_acell("B" + str(r), "")
        sheet.update_acell("C" + str(r), "")
    return row1
        
        
def player_check(chat_id):
    row_no = sheet.findall(str(chat_id), in_column=1)
    if(len(row_no)==0):
        return False
    elif(len(row_no) == 1):
        return row_no[0]
    else:
        row_no = purge_row(row_no)
        return row_no


def update_score(chat_id, name):
    check = player_check(chat_id)
    if not check:
        sheet.append_row([chat_id, name, 1])
    elif type(check).__name__ == "int":
        cell = "C" + str(check)
        score = sheet.acell(cell, value_render_option='FORMATTED_VALUE').value
        sheet.update_acell(cell, str(int(score) + 1))
    else:
        update_score(chat_id, name)


def get_score(chat_id):
    row_no = player_check(chat_id)
    if not row_no:
        return 0
    else:
        cell = "C" + str(row_no)
        score = sheet.acell(cell, value_render_option='FORMATTED_VALUE').value
        return score



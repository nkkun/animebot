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


def player_check(chat_id):
    try:
        row_no = sheet.find(str(chat_id), in_column=1).row
    except Exception as e:
        if(type(e).__name__ == 'CellNotFound'):
            row_no = False
        else:
            row_no = "redo"
    if row_no == "redo":
        player_check(chat_id)
    else:
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



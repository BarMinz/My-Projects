import time
import pandas as pd
import pywhatkit
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

URL = 'https://docs.google.com/spreadsheets/d/1wU1346u_6U1VV9pxPRyRtv7OBucfnErKDUiUqWTwzSQ/export?format=csv&gid=567420253' # Need to create a second sheet in the url 
PHONE_NUMS = [os.environ['PHONE_NUM1'], os.environ['PHONE_NUM2']]


def get_message() -> str:
    read_file = pd.read_csv(URL) 
    file_content = read_file.to_dict(orient='records')
    msg = file_content[0]['message']
    return msg


def time_whatsapp_msg(contact_list, msg):
    time_to_send = input("Enter time to send message (in 24 hours format): ")
    hour = time_to_send.split(':')[0]
    minutes = time_to_send.split(':')[1]
    for contact in contact_list:
        pywhatkit.sendwhatmsg(contact, msg, hour, minutes, tab_close = True)
        

def send_whatsapp_msg(contact, msg):
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    pywhatkit.sendwhatmsg(contact, msg, current_hour, current_minute+1, tab_close = True)
        


if __name__ == '__main__':
    msg = get_message()
    for num in PHONE_NUMS:
        send_whatsapp_msg(num, msg)
        time.sleep(60)

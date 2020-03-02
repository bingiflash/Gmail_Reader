from tkinter import *
from multiprocessing import *
import imaplib
import email
from dateutil.parser import parse
from datetime import timedelta
import os
import sys
import time
import ctypes
from credentials import Email, App_password

# weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def visual_notification(notification):
    reply = ctypes.windll.user32.MessageBoxW(
        0, "You have a new message", "Mail Update", 1)
    # while(reply != 1):
    #     reply = ctypes.windll.user32.MessageBoxW(
    #         0, "New Email", "Mail Update", 1)
    # if reply == 1:
    notification.value = False


def audible_notification(notification):
    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id)
    # sen = 'New Email'
    while notification.value != False:
        os.system("espeak \""+"You have a new message"+"\"")
        # engine.say(sen)
        # engine.runAndWait()


def main():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(Email,
               App_password)  # App Password
    mail.select("inbox")
    status, data = mail.search(None, 'unseen', 'OR', 'OR', 'FROM', 'nathreyas@sperodevices.com',  'FROM',
                               'jgupta@sperodevices.com', 'OR', 'FROM', 'consult-mg@gstardust.com', 'FROM', 'mg@gstardust.com')

    # print(data)

    ids = data[0]
    id_list = ids.split()

    if len(id_list) is 0:
        print("No new messages")
    else:
        # print("\n\n\n\n\n\n\n\n")
        # print("          /\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\")
        # print("                                                 You have a new message")
        # print("          /\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\")
        notification = Value('b', True)
        p1 = Process(target=visual_notification, args=(notification,))
        p2 = Process(target=audible_notification, args=(notification,))

        p2.start()
        p1.start()
        p1.join()
        p2.join()
        # os.system("espeak \""+"You have a new message"+"\"")
        # time.sleep(2)
        # for i in range(1, len(id_list)+1):
        #     email_id = id_list[-1*i]  # Getting latest Email's id
        #     status, data = mail.fetch(email_id, "(RFC822)")
        #     raw_email = data[0][1]
        #     email_message = email.message_from_bytes(raw_email)
        #     sender = email.utils.parseaddr(
        #         email_message['From'])[0]
        #     # print(sender)
        #     text = "Mail from "+sender
        #     os.system("espeak \""+text+"\"")
        #     mail.store(id_list[-1*i], '-FLAGS', '\Seen')
        # print('{0: <35}'.format(email.utils.parseaddr(
        #     sender)[0]), end="")
        # print('{0: <60}'.format(email_message['Subject']), end="")
        # # Converting GMT to EST (EST = GMT - 5h)
        # date_obj = parse(email_message['Date'])
        # print('{0: <10}'.format(
        #     str(weekdays[date_obj.weekday()]) + " " + str(date_obj.strftime("%Y %m %d %I:%M %p"))))
        # mail.store(id_list[-1*i], '+FLAGS', '\Seen')
        # # mail.store(id_list[-1*i], '+FLAGS', '\Recent')


if __name__ == "__main__":
    while True:
        notification = Value('b', True)
        main()
        time.sleep(300)  # 5 minutes

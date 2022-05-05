import random
import smtplib
import time
import datetime
import getpass
import threading
import os


LOADED = 0

load2 = list("/-\|")
load = [".", "..", "...", "   "]


def loading(i, type):
    if type == 1:
        time.sleep(0.5)
        return load[i%len(load)]
    else:
        time.sleep(0.2)
        return load2[i%len(load2)]


def loader(text="Please wait", type=1):
    global LOADED
    i = 0
    if type == 1:
        while not LOADED:
            print(f"{text}{loading(i, type)}", end="\r")
            i += 1
    else:
        while not LOADED:
            print(f"{text}...{loading(i, type)}", end="\r")
            i += 1

    LOADED = 0


OTP_LENGTH = 4
TIME_LIMIT = 60

PASSWORD = os.environ.get("PASSWORD")
EMAIL = os.environ.get("EMAIL")

OTP = ''

def get_otp():
    global OTP
    OTP = ""
    for _ in range(OTP_LENGTH):
        OTP += str(random.randint(0, 9))
    return OTP


def send_otp(user_email):
    global LOADED
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(EMAIL, PASSWORD)

    subject = 'OTP for authentication.'
    body = f'{get_otp()} is your One-Time Password valid till {set_time_limit()}.\nDO NOT SHARE THIS WITH ANYONE.'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        EMAIL,
        f'{user_email}',
        msg
    )
    server.quit()
    LOADED = 1


def set_time_limit():
    time_now = (str(datetime.datetime.now()))[11:19]

    hour_now = int(time_now[:2])
    min_now = int(time_now[3:5])
    sec_now = int(time_now[6:8])

    Sec = str((TIME_LIMIT) % 60)
    Min = str(((TIME_LIMIT) // 60) % 60)
    Hour = str(((TIME_LIMIT) // (60*60)) % 24)

    fsec = str((sec_now + int(Sec)) % 60)
    fmin = str((min_now + int(Min)) % 60)
    fhour = str((hour_now + int(Hour)) % 24)

    if len(fsec) < 2:
        fsec = '0' + fsec

    if len(fmin) < 2:
        fmin = '0' + fmin

    if len(fhour) < 2:
        fhour = '0' + fhour

    fTime = ':'.join([fhour, fmin, fsec])
    return fTime


auth = False


def authenticate(input_otp, time):
    global OTP
    if time <= TIME_LIMIT:
        if input_otp == OTP:
            print("Authenticated successfully!")
            auth = True

        else:
            print("Entered OTP is incorrect. Please try again.")
            auth = False
    else:
        print("OTP timed out!")
        auth = False

    return auth


def execute(user_email):
    global LOADED
    set_time_limit()
    start_time = time.time()
    mail_thread = threading.Thread(target=send_otp, args=(user_email,))
    mail_thread.start()
    loader(type=2)
    input_otp = getpass.getpass(f"Please enter the OTP sent to {user_email}:\n>")
    end_time = time.time()
    Time = end_time - start_time

    auth = authenticate(input_otp, Time)
    return auth


if __name__ == "__main__":
    execute(input("Enter your email address --> "))

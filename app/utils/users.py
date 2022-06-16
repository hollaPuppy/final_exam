import os
import hashlib
import smtplib
import ujson

from random import randint

from config import EMAIL_PASSWORD


async def hash_password(user_password: str) -> dict:
    salt = os.urandom(32).hex()
    key = hashlib.pbkdf2_hmac("sha256", user_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

    return {"salt": salt, "key": key}


async def check_password_hash(user_password: str, password_hash: str) -> bool:
    password_hash = ujson.loads(password_hash)
    salt, key = password_hash["salt"], password_hash["key"]
    new_key = hashlib.pbkdf2_hmac("sha256", user_password.encode("utf-8"), salt.encode("utf-8"), 100000).hex()

    return key == new_key


async def send_confirm_letter(email: str) -> str:
    conf_code = str(randint(1000, 9999))
    text_mail = f"Please, do not reply to this message!\nYour confirm code: {conf_code}."

    sender = "bestgamenoreply@gmail.com"
    password = EMAIL_PASSWORD
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, email, f"Subject: Confirm code\n{text_mail}")
    except Exception as _ex:
        return f"{_ex}\n Check account data pls"

    return conf_code


async def parse_active_time(profile_list: dict):
    raw_active_time = int(profile_list.get('user_active_time'))
    dict_time = {'hours': 0, 'minutes': 0, 'seconds': 0}
    if raw_active_time >= 60:
        if raw_active_time >= 3600:
            dict_time['hours'] = raw_active_time // 3600
            raw_active_time = raw_active_time % 3600
        dict_time['minutes'] = raw_active_time // 60
        dict_time['seconds'] = raw_active_time % 60
    profile_list['user_active_time'] = dict_time

    return profile_list

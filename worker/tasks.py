from .worker_config import worker_cel 
import smtplib
import os

@worker_cel.task()
def task_send_cofirm_letter(target_email: str, code: str):
    conf_code = code
    text_mail = f"Please, do not reply to this message!\nYour confirm code: {conf_code}."

    sender = os.getenv('CONFIG_EMAIL_SMTP')
    password = os.getenv('CONFIG_PASSWORD_SMTP')
    
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

    try:
        server.login(sender, password)
        server.sendmail(sender, target_email, f"Subject: Confirm code\n{text_mail}")
        server.quit()
    except Exception as _ex:
        return f"{_ex}\n Check account data pls"

    return 'ok'
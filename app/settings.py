import os

DATABASE_URL: str = os.getenv('DATA_BASE_URL')
if not DATABASE_URL:
    from config import CONFIG_DATABASE_URL

    DATABASE_URL = CONFIG_DATABASE_URL

EMAIL_EXAMPLE = "emailname@email.ru"


EMAIL_PASSWORD: str = os.getenv('EMAIL_PASS_WORD')
if not EMAIL_PASSWORD:
    from config import CONFIG_EMAIL_PASSWORD

    EMAIL_PASSWORD = CONFIG_EMAIL_PASSWORD

EMAIL_EXAMPLE = "emailname@email.ru"
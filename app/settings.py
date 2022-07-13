import os

DATABASE_URL: str = os.getenv('DATABASE_URL_LOCAL')
if not DATABASE_URL:
    from config import CONFIG_DATABASE_URL

    DATABASE_URL = CONFIG_DATABASE_URL


PASSWORD_EXAMPLE = 'qaz1xsw2edc3'

EMAIL_EXAMPLE = 'testmail@mail.ru'

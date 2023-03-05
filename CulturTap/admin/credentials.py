from pydantic import BaseSettings
from os import getcwd


class Settings(BaseSettings):
    DB_URL: str
    DB_API: str
    SMSID: str
    SMSTOKEN: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    MID: str
    KEY: str
    CLIENT_ID: str
    WEBSITE: str
    CALLBACK_URL: str
    ENVIRONMENT: str
    APP_ID: str
    APP_CERTIFICATE: str
    TOKEN : str

    class Config:
        env_file =getcwd()+r'\CulturTap\admin\.env'


settings = Settings()

TOKEN = settings.TOKEN

# Database
DB_URL = settings.DB_URL
DB_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': settings.DB_API,
}

# SMS
SMSID = settings.SMSID
SMSTOKEN = settings.SMSTOKEN

# AWS S3
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

# Paytm
MID = settings.MID
KEY = settings.KEY
CLIENT_ID = settings.CLIENT_ID
WEBSITE = settings.WEBSITE
CALLBACK_URL = settings.CALLBACK_URL
ENVIRONMENT = settings.ENVIRONMENT
# For Production
# CALLBACK_URL = https://securegw.paytm.in/theia/paytmCallback
# environment = LibraryConstants.PRODUCTION_ENVIRONMENT

# Agora
APP_ID = settings.APP_ID
APP_CERTIFICATE = settings.APP_CERTIFICATE

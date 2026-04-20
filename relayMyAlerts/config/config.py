from os import environ

class Config:

    ENV = environ.get("RMA_ENV", "production")

    DEBUG = int(environ.get("RMA_DEBUG", "0"))

    TESTING = int(environ.get("RMA_TESTING", "0"))

    TIMEOUT = int (environ.get("RMA_TIMEOUT", "30"))

    RETRY = int (environ.get("RMA_RETRY", "5"))

    ########## MatterMost ##########

    MATTERMOST_ENABLED = int(environ.get("RMA_MATTERMOST_ENABLED","0"))

    MATTERMOST_WEBHOOK_URL = environ.get("RMA_MATTERMOST_WEBHOOK_URL","")

    ########## Zulip ##########

    ZULIP_ENABLED = int(environ.get("RMA_ZULIP_ENABLED","0"))

    ZULIP_API_URL = environ.get("RMA_ZULIP_API_URL","")

    ZULIP_BOT_EMAIL = environ.get("RMA_ZULIP_BOT_EMAIL","")

    ZULIP_API_KEY = environ.get("RMA_ZULIP_API_KEY","")

    ZULIP_CHANNEL = environ.get("RMA_ZULIP_CHANNEL","")

    ZULIP_TOPIC = environ.get("RMA_ZULIP_TOPIC","Alerting")

    ########## Zoho ##########

    ZOHO_ENABLED = int(environ.get("RMA_ZOHO_ENABLED","0"))

    ZOHO_WEBHOOK_URL = environ.get("RMA_ZOHO_WEBHOOK_URL","")
    




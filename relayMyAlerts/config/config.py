from os import environ

class Config:

    ENV = environ.get("RMA_ENV", "production")

    DEBUG = int(environ.get("RMA_DEBUG", "0"))

    TESTING = int(environ.get("RMA_TESTING", "0"))

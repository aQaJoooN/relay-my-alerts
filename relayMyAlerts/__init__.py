from flask import Flask

from relayMyAlerts.config import Config

# Application factory
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # Load configs from ENV variables.
    return app
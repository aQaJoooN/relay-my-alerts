from flask import jsonify
import logging
from relayMyAlerts.config import Config
from relayMyAlerts.util import create_message


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ZulipController:
    def create_zulip_message():
        """
        Docstring for create_zulip_message
        """
        return create_message("zulip")

    
    def list_zulip_config():
        return jsonify({"ZULIP_API_KEY": len(Config.ZULIP_API_KEY) * "*" , 
                        "ZULIP_API_URL": Config.ZULIP_API_URL, 
                        "ZULIP_BOT_EMAIL": Config.ZULIP_BOT_EMAIL, 
                        "ZULIP_CHANNEL": Config.ZULIP_CHANNEL, 
                        "ZULIP_TOPIC": Config.ZULIP_TOPIC})

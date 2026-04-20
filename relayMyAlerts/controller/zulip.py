from flask import jsonify
from relayMyAlerts.config import Config
from relayMyAlerts.util import create_message
import inspect

class ZulipController:
    def create_zulip_message():
        """
        Docstring for create_zulip_message
        """
        if Config.ZULIP_ENABLED == 1:
            return create_message("zulip")
        elif inspect.currentframe().f_back.f_code.co_name == "create_message":
            return {"info": "Zulip is not Enabled"},200
        else:
            return {"error": "Zulip is not Enabled"},500

    
    def list_zulip_config():
        return jsonify({"ZULIP_ENABLED": Config.ZULIP_ENABLED, 
                        "ZULIP_API_KEY": len(Config.ZULIP_API_KEY) * "*" , 
                        "ZULIP_API_URL": Config.ZULIP_API_URL, 
                        "ZULIP_BOT_EMAIL": Config.ZULIP_BOT_EMAIL, 
                        "ZULIP_CHANNEL": Config.ZULIP_CHANNEL, 
                        "ZULIP_TOPIC": Config.ZULIP_TOPIC})

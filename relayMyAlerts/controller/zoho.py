from flask import jsonify
from relayMyAlerts.config import Config
from relayMyAlerts.util import create_message
import inspect

class ZohoController:
    def create_zoho_message():
        """
        Docstring for create_zoho_message
        """
        if Config.ZOHO_ENABLED == 1:
            return create_message("zoho")
        elif inspect.currentframe().f_back.f_code.co_name == "create_message":
            return {"info": "Zoho is not Enabled"},200
        else:
            return {"error": "Zoho is not Enabled"},500
    
    def list_zoho_config():
        parts = Config.ZOHO_WEBHOOK_URL.split("zapikey=")
        token = "*" * len(parts[1])
        zoho_hidden_url = parts[0] + "hooks/" + token
        return jsonify({"ZOHO_ENABLED": Config.ZOHO_ENABLED,
                        "ZOHO_WEBHOOK_URL": zoho_hidden_url})
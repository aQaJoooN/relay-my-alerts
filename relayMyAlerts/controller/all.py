from flask import abort,request,jsonify
import logging
from relayMyAlerts.config import Config
from relayMyAlerts.controller import MattermostController
from relayMyAlerts.controller import ZohoController
from relayMyAlerts.controller import ZulipController

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AllController:
    def create_message():
        """
        Docstring for create_message
        """
        if request.content_type != "application/json":
            abort(415)
        data = request.get_json()
        if not data:
            abort(400)
        logging.info(f"Received message data for all")
        
        allResults = ({
            "zulip": ZulipController.create_zulip_message(),
            "mattermost": MattermostController.create_mattermost_message(),
            "zoho": ZohoController.create_zoho_message()
        })

        if allResults["zulip"][1] == 200 and allResults["mattermost"][1] == 200 and allResults["zoho"][1] == 200:
            return {"overall_status": "success", "details":allResults}, 200
        elif allResults["zulip"][1] != 200 and allResults["mattermost"][1] != 200 and allResults["zoho"][1] != 200:
            return {"overall_status": "error", "details":allResults}, 500
        else:
            return {"overall_status": "partial_success", "details":allResults}, 500
    
    def list_config():
        parts = Config.MATTERMOST_WEBHOOK_URL.split("hooks/")
        token = "*" * len(parts[1])
        mattermost_hidden_url = parts[0] + "hooks/" + token
        parts = Config.ZOHO_WEBHOOK_URL.split("zapikey=")
        token = "*" * len(parts[1])
        zoho_hidden_url = parts[0] + "hooks/" + token
        return jsonify({"ZULIP_ENABLED": Config.ZULIP_ENABLED,
                        "ZULIP_API_KEY": len(Config.ZULIP_API_KEY) * "*" , 
                        "ZULIP_API_URL": Config.ZULIP_API_URL, 
                        "ZULIP_BOT_EMAIL": Config.ZULIP_BOT_EMAIL, 
                        "ZULIP_CHANNEL": Config.ZULIP_CHANNEL, 
                        "ZULIP_TOPIC": Config.ZULIP_TOPIC, 
                        "MATTERMOST_ENABLED": Config.MATTERMOST_ENABLED,
                        "MATTERMOST_WEBHOOK_URL": mattermost_hidden_url, 
                        "ZOHO_ENABLED": Config.ZOHO_ENABLED,
                        "ZOHO_WEBHOOK_URL": zoho_hidden_url,
                        "RETRY": Config.RETRY, 
                        "TIMEOUT": Config.TIMEOUT, 
                        "TESTING": Config.TESTING, 
                        "DEBUG": Config.DEBUG, 
                        "ENV": Config.ENV})
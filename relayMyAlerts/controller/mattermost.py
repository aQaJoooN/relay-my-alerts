from flask import jsonify
from relayMyAlerts.config import Config
from relayMyAlerts.util import create_message
import inspect

class MattermostController:
    def create_mattermost_message():
        """
        Docstring for create_mattermost_message
        """
        if Config.MATTERMOST_ENABLED == 1:
            return create_message("mattermost")
        elif inspect.currentframe().f_back.f_code.co_name == "create_message":
            return {"info": "Mattermost is not Enabled"},200
        else:
            return {"error": "Mattermost is not Enabled"},500
    
    def list_mattermost_config():
        parts = Config.MATTERMOST_WEBHOOK_URL.split("hooks/")
        token = "*" * len(parts[1])
        hidden_url = parts[0] + "hooks/" + token
        return jsonify({"MATTERMOST_ENABLED": Config.MATTERMOST_ENABLED,
                        "MATTERMOST_WEBHOOK_URL": hidden_url})
from flask import jsonify
import logging
from relayMyAlerts.config import Config
from relayMyAlerts.util import create_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MattermostController:
    def create_mattermost_message():
        """
        Docstring for create_mattermost_message
        """
        return create_message("mattermost")
    
    def list_mattermost_config():
        parts = Config.MATTERMOST_WEBHOOK_URL.split("hooks/")
        token = "*" * len(parts[1])
        hidden_url = parts[0] + "hooks/" + token
        return jsonify({"MATTERMOST_WEBHOOK_URL": hidden_url})
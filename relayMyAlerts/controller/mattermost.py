import time
from flask import abort,request,jsonify
import requests
import logging
from relayMyAlerts.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MattermostController:
    def create_mattermost_message():
        """
        Docstring for create_mattermost_message
        """
        if request.content_type != "application/json":
            abort(415)
        data = request.get_json()
        if not data:
            abort(400)
        if not hasattr(Config, 'MATTERMOST_WEBHOOK_URL') or not Config.MATTERMOST_WEBHOOK_URL:
            logging.error("RMA_MATTERMOST_WEBHOOK_URL not configured")
            return {"error": "Webhook URL not configured"}, 500
        
        logging.info(f"Received message data for mattermost: {data}")

        # decorate massage
        message = f"🔥 *Alert:* {data}"

        result = None
        for attempt in range(Config.RETRY):
            time.sleep(1)
            result = MattermostController.send_mattermost(message)
            if result["status"] in ("success", "skipped"):
                return result, 200
            else:
                logging.warning(f"Mattermost send failed. retry attempt: {attempt + 1} .")
        
        return result, 500

    def send_mattermost(message_content):
        """
        Sends a message to Mattermost using a webhook.
        """
        payload = {
            # decorate mattermost message 
            "text": message_content
        }
        # Use a session for potential reuse and setting verify=False - disable ssl if necassary
        session = requests.Session()
        #session.verify = False
        session.verify = True
        try:
            resp = session.post(
                Config.MATTERMOST_WEBHOOK_URL, 
                json=payload, 
                timeout=Config.TIMEOUT)
            #resp.raise_for_status()
            if resp.status_code == 200:
                logging.info(f"Mattermost response: {resp.text}")
                return {"service": "mattermost", "status": "success", "message": "Alert sent successfully."}
            else:
                logging.error(f"Mattermost error: {resp.status_code} - {resp.text}")
                return {"service": "mattermost", "status": "error"}
        except requests.exceptions.RequestException as e:
            logging.error(f"Mattermost Connection Error: {e}")
            return {"service": "mattermost", "status": "error"}
    
    def list_mattermost_config():
        parts = Config.MATTERMOST_WEBHOOK_URL.split("hooks/")
        token = "*" * len(parts[1])
        hidden_url = parts[0] + "hooks/" + token
        return jsonify({"MATTERMOST_WEBHOOK_URL": hidden_url})
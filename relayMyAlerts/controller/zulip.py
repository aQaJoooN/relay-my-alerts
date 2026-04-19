import time
from flask import abort,request,jsonify
import requests
import logging
from relayMyAlerts.config import Config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ZulipController:
    def create_zulip_message():
        """
        Docstring for create_zulip_message
        """
        if request.content_type != "application/json":
            abort(415)
        data = request.get_json()
        if not data:
            abort(400)
        if not hasattr(Config, 'ZULIP_API_URL') or not Config.ZULIP_API_URL:
            logging.error("RMA_ZULIP_API_URL not configured")
            return {"error": "Zulip Api URL not configured"}, 500
        if not hasattr(Config, 'ZULIP_BOT_EMAIL') or not Config.ZULIP_BOT_EMAIL:
            logging.error("RMA_ZULIP_BOT_EMAIL not configured")
            return {"error": "Zulip Bot Email not configured"}, 500
        if not hasattr(Config, 'ZULIP_API_KEY') or not Config.ZULIP_API_KEY:
            logging.error("RMA_ZULIP_API_KEY not configured")
            return {"error": "Zulip Api Key not configured"}, 500
        if not hasattr(Config, 'ZULIP_CHANNEL') or not Config.ZULIP_CHANNEL:
            logging.error("RMA_ZULIP_CHANNEL not configured")
            return {"error": "Zulip Channel not configured"}, 500
        
        logging.info(f"Received message data for Zulip: {data}")

        # decorate massage
        message = f"🔥 *Alert:* {data}"

        result = None
        for attempt in range(Config.RETRY):
            time.sleep(1)
            result = ZulipController.send_zulip(message)
            if result["status"] in ("success", "skipped"):
                return result, 200
            else:
                logging.warning(f"Zulip send failed. retry attempt: {attempt + 1} .")
        
        return result, 500

    def send_zulip(message_content):
        """
        Sends a message to Zulip using a webhook.
        """
        payload = {
            "type": "channel",
            "to": Config.ZULIP_CHANNEL,
            "topic": Config.ZULIP_TOPIC,
            "content": message_content
        }
        # Use a session for potential reuse and setting verify=False - disable ssl if necassary
        session = requests.Session()
        session.verify = False
        #session.verify = True
        try:
            resp = session.post(
                Config.ZULIP_API_URL, 
                data=payload, 
                auth=(Config.ZULIP_BOT_EMAIL, Config.ZULIP_API_KEY), 
                timeout=Config.TIMEOUT
                )
            #resp.raise_for_status()
            if resp.status_code == 200:
                logging.info(f"Zulip response: {resp.text}")
                return {"service": "zulip", "status": "success", "message": "Alert sent successfully."}
            else:
                logging.error(f"Zulip error: {resp.status_code} - {resp.text}")
                return {"service": "Zulip", "status": "error"}
        except requests.exceptions.RequestException as e:
            logging.error(f"Zulip Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Zulip error response: {e.response.status_code} - {e.response.text}")
            return {"service": "zulip", "status": "error"}
    
    def list_zulip_config():
        return jsonify({"ZULIP_API_KEY": len(Config.ZULIP_API_KEY) * "*" , 
                        "ZULIP_API_URL": Config.ZULIP_API_URL, 
                        "ZULIP_BOT_EMAIL": Config.ZULIP_BOT_EMAIL, 
                        "ZULIP_CHANNEL": Config.ZULIP_CHANNEL, 
                        "ZULIP_TOPIC": Config.ZULIP_TOPIC})

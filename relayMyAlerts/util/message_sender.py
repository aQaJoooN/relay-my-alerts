import time
from flask import abort,request
import requests
import logging
from relayMyAlerts.config import Config
from relayMyAlerts.util.decorator import alert_decorator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_message(im):
    """
    create message template
    """
    if request.content_type != "application/json":
        abort(415)
    data = request.get_json()
    if not data:
        abort(400)
    if im == "mattermost":
        if not hasattr(Config, 'MATTERMOST_WEBHOOK_URL') or not Config.MATTERMOST_WEBHOOK_URL:
            logging.error("RMA_MATTERMOST_WEBHOOK_URL not configured")
            return {"error": "Webhook URL not configured"}, 500
    elif im == "zulip":
        if not hasattr(Config, 'ZULIP_API_URL') or not Config.ZULIP_API_URL:
            logging.error("RMA_ZULIP_API_URL not configured")
            return {"error": "Zulip Api URL not configured"}, 500
        elif not hasattr(Config, 'ZULIP_BOT_EMAIL') or not Config.ZULIP_BOT_EMAIL:
            logging.error("RMA_ZULIP_BOT_EMAIL not configured")
            return {"error": "Zulip Bot Email not configured"}, 500
        elif not hasattr(Config, 'ZULIP_API_KEY') or not Config.ZULIP_API_KEY:
            logging.error("RMA_ZULIP_API_KEY not configured")
            return {"error": "Zulip Api Key not configured"}, 500
        elif not hasattr(Config, 'ZULIP_CHANNEL') or not Config.ZULIP_CHANNEL:
            logging.error("RMA_ZULIP_CHANNEL not configured")
            return {"error": "Zulip Channel not configured"}, 500
    elif im == "zoho":
        if not hasattr(Config, 'ZOHO_WEBHOOK_URL') or not Config.ZOHO_WEBHOOK_URL:
            logging.error("RMA_ZOHO_WEBHOOK_URL not configured")
            return {"error": "Zoho URL not configured"}, 500
    else:
        return {"service": im, "status": "error", "message": "Instant messaging service is not implemented yet."}, 500
    
    message = None
    if "alerts" in data:
        message = alert_decorator(data)
    else:
        message = f"non structured input: {data}"

    logging.info(f"Received message data for {im} : {message}")

    result = None
    for attempt in range(Config.RETRY):
        time.sleep(1)
        result = send_message(im,message)
        if result["status"] in ("success", "skipped"):
            return result, 200
        else:
            logging.warning(f"{im} send failed. retry attempt: {attempt + 1} .")
    
    return result, 500

def send_message(im,message_content):
    """
    Sends a message to a given webhook.
    """
    
    # Use a session for potential reuse and setting verify=False - disable ssl if necassary
    session = requests.Session()
    session.verify = False
    #session.verify = True

    payload = None
    resp = None
    if im == "zulip":
        payload = {
            "type": "channel",
            "to": Config.ZULIP_CHANNEL,
            "topic": Config.ZULIP_TOPIC,
            "content": message_content
        }
        resp = session.post(
            Config.ZULIP_API_URL, 
            data=payload, 
            auth=(Config.ZULIP_BOT_EMAIL, Config.ZULIP_API_KEY), 
            timeout=Config.TIMEOUT
            )
    elif im == "mattermost":
        payload = {
            "text": message_content
        }
        resp = session.post(
            Config.MATTERMOST_WEBHOOK_URL, 
            json=payload, 
            timeout=Config.TIMEOUT)
    elif im == "zoho":
        payload = {
            "text": message_content
        }
        resp = session.post(
            Config.ZOHO_WEBHOOK_URL, 
            json=payload, 
            timeout=Config.TIMEOUT)
    else:
        return {"service": im, "status": "error", "message": "Instant messaging service is not implemented yet."}
    try:
        #resp.raise_for_status()
        if resp.status_code == 200:
            logging.info(f"{im} response: {resp.text}")
            return {"service": im, "status": "success", "message": "Alert sent successfully."}
        else:
            logging.error(f"{im} error: {resp.status_code} - {resp.text}")
            return {"service": im, "status": "error"}
    except requests.exceptions.RequestException as e:
        logging.error(f"{im} Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"{im} error response: {e.response.status_code} - {e.response.text}")
        return {"service": im, "status": "error"}
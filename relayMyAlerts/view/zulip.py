from flask_restful import Resource

from relayMyAlerts.controller import ZulipController

class ZulipResource(Resource):

    def get(self):
        return ZulipController.list_zulip_config()
    def post(self):
        return ZulipController.create_zulip_message()
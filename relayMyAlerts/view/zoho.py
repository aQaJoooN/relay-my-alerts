from flask_restful import Resource

from relayMyAlerts.controller import ZohoController

class ZohoResource(Resource):

    def get(self):
        return ZohoController.list_zoho_config()
    def post(self):
        return ZohoController.create_zoho_message()
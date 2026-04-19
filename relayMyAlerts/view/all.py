from flask_restful import Resource

from relayMyAlerts.controller import AllController

class AllResource(Resource):

    def get(self):
        return AllController.list_config()
    def post(self):
        return AllController.create_message()
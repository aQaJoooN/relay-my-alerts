from flask_restful import Resource

from relayMyAlerts.controller import MattermostController

class MattermostResource(Resource):

    def get(self):
        return MattermostController.list_mattermost_config()
    def post(self):
        return MattermostController.create_mattermost_message()
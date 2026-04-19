from relayMyAlerts import api

from relayMyAlerts.view.mattermost import MattermostResource
from relayMyAlerts.view.zulip import ZulipResource
from relayMyAlerts.view.all import AllResource

api.add_resource(
    MattermostResource,
    "/mattermost",
    methods=["GET","POST"],
    endpoint="mattermost"
)

api.add_resource(
    ZulipResource,
    "/zulip",
    methods=["GET","POST"],
    endpoint="zulip"
)

api.add_resource(
    AllResource,
    "/all",
    methods=["GET","POST"],
    endpoint="all"
)
import json
import getpass
from ..application_settings import ApplicationSettings


class IdentifyNetworkElementHandler:
    def __init__(self, websocket):
        self.websocket = websocket
        self.settings = ApplicationSettings()

    def handle(self, identified_feature_id, selected_type):
        response = {
            "eventType": "IdentifyNetworkElement",
            "identifiedFeatureId": identified_feature_id,
            "selectedType": selected_type,
            "username": self.settings.get_user_name_prefix()
        }

        self.websocket.send(json.dumps(response))

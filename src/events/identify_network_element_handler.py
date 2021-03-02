import json
import getpass


class IdentifyNetworkElementHandler:
    def __init__(self, websocket):
        self.websocket = websocket

    def handle(self, identified_feature_id, selected_type):
        response = {
            "eventType": "IdentifyNetworkElement",
            "identifiedFeatureId": identified_feature_id,
            "selectedType": selected_type,
            "username": getpass.getuser()
        }

        self.websocket.send(json.dumps(response))

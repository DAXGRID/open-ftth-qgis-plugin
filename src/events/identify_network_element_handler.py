import json

class IdentifyNetworkElementHandler:
    def __init__(self, websocket):
        self.websocket = websocket

    def handle(self, identified_feature_id):
        response = {
            "eventType": "IdentifyNetworkElement",
            "identifiedFeatureId": identified_feature_id
        }

        self.websocket.send(json.dumps(response))

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
            "username": self.settings.get_user_name_suffix()
        }

        self.websocket.send(json.dumps(response))

    # This is made to handle 'RetrieveIdentifiedNetworkElement' message-request
    # and that contains a username, and only that username wants the identified-feature.
    def handle_message(self, identified_feature_id, selected_type, message):
        if message.username != self.settings.get_user_name_suffix():
            return

        self.handle(identified_feature_id, selected_type)

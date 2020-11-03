import json
import getpass

class RetrieveSelectedHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket

    def handle(self, message):
        if message.username != getpass.getuser():
            return

        selected_features = self.iface.mapCanvas().currentLayer().selectedFeatures()

        selected_features_mrids = []
        for selected_feature in selected_features:
            mrid = selected_feature.attribute("mrid")
            selected_features_mrids.append(mrid)

        response = {
            "eventType": "RetrieveSelectedResponse",
            "selectedFeaturesMrid": selected_features_mrids,
            "username": getpass.getuser()
        }

        self.websocket.send(json.dumps(response))

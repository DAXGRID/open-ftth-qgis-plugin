import json

class GetSelectedFeaturesHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket

    def handle(self):
        selected_features = self.iface.mapCanvas().currentLayer().selectedFeatures()
        selected_features_mrids = []

        for selected_feature in selected_features:
            mrid = selected_feature.attribute("mrid")
            selected_features_mrids.append(mrid)

        response = {
            "eventType": "GetSelectedFeaturesResponse",
            "selectedFeaturesMrid": selected_features_mrids
        }

        self.websocket.send(json.dumps(response))

import json
import getpass
from ..application_settings import ApplicationSettings
from qgis.core import QgsProject


class RetrieveSelectedHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket
        self.settings = ApplicationSettings()

    def handle(self, message):
        if message.username != self.settings.get_user_name_prefix():
            return

        selected_features = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_segment_name())[0].getSelectedFeatures()

        selected_features_mrids = []
        for selected_feature in selected_features:
            mrid = selected_feature.attribute("mrid")
            selected_features_mrids.append(mrid)

        response = {
            "eventType": "RetrieveSelectedResponse",
            "selectedFeaturesMrid": selected_features_mrids,
            "username": self.settings.get_user_name_prefix()
        }

        self.websocket.send(json.dumps(response))

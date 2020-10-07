import json
import base64
from types import SimpleNamespace
from .events.geographical_area_updated_handler import GeographicalAreaUpdatedHandler
from .events.get_selected_features_handler import GetSelectedFeaturesHandler

class EventHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket
        self.geographicalAreaUpdatedHandler = GeographicalAreaUpdatedHandler(self.iface)
        self.getSelectedFeaturesHandler = GetSelectedFeaturesHandler(self.iface, self.websocket)

    def handle(self, message):
        json = base64.b64decode(message);
        deserializedObject = self.deserialize(json);

        if deserializedObject.eventType == "ObjectsWithinGeographicalAreaUpdated":
            self.geographicalAreaUpdatedHandler.handle()
        elif deserializedObject.eventType == "GetSelectedFeatures":
            self.getSelectedFeaturesHandler.handle()
            
    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

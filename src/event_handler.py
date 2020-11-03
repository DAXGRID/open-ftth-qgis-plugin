import json
import base64
from types import SimpleNamespace
from .events.geographical_area_updated_handler import GeographicalAreaUpdatedHandler
from .events.retrieve_selected_handler import RetrieveSelectedHandler

class EventHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket
        self.geographicalAreaUpdatedHandler = GeographicalAreaUpdatedHandler(self.iface)
        self.getSelectedFeaturesHandler = RetrieveSelectedHandler(self.iface, self.websocket)

    def handle(self, message):
        deserializedObject = self.deserialize(message);

        if deserializedObject.eventType == "ObjectsWithinGeographicalAreaUpdated":
            self.geographicalAreaUpdatedHandler.handle()
        elif deserializedObject.eventType == "RetrieveSelected":
            self.getSelectedFeaturesHandler.handle(deserializedObject)
            
    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

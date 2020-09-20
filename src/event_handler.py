import json
import base64
from types import SimpleNamespace
from .events.geographical_area_updated_handler import GeographicalAreaUpdatedHandler

class EventHandler:
    def __init__(self, iface):
        self.iface = iface

    def handle(self, message):
        json = base64.b64decode(message);
        deserializedObject = self.deserialize(json);

        if deserializedObject.eventType == "ObjectsWithinGeographicalAreaUpdated":
            GeographicalAreaUpdatedHandler(self.iface).handle();
            
    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

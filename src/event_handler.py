import json
from types import SimpleNamespace
from .events.geographical_area_updated_handler import GeographicalAreaUpdatedHandler
from .events.retrieve_selected_handler import RetrieveSelectedHandler
from .events.pan_to_coordinate_handler import PanToCoordinateHandler
from .events.highlight_features_handler import HighlightFeaturesHandler


class EventHandler:
    def __init__(self, iface, websocket):
        self.iface = iface
        self.websocket = websocket
        self.geographicalAreaUpdatedHandler = GeographicalAreaUpdatedHandler(self.iface)
        self.getSelectedFeaturesHandler = RetrieveSelectedHandler(self.iface, self.websocket)
        self.panToCoordinateHandler = PanToCoordinateHandler(self.iface)
        self.highlightFeaturesHandler = HighlightFeaturesHandler(self.iface)

    def handle(self, message):
        deserializedObject = self.deserialize(message);

        if deserializedObject.eventType == "ObjectsWithinGeographicalAreaUpdated":
            self.geographicalAreaUpdatedHandler.handle()
        elif deserializedObject.eventType == "RetrieveSelected":
            self.getSelectedFeaturesHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "PanToCoordinate":
            self.panToCoordinateHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "HighlightFeatures":
            self.highlightFeaturesHandler.handle(deserializedObject)

    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

import json
from types import SimpleNamespace
from .events.geographical_area_updated_handler import GeographicalAreaUpdatedHandler
from .events.retrieve_selected_handler import RetrieveSelectedHandler
from .events.pan_to_coordinate_handler import PanToCoordinateHandler
from .events.highlight_features_handler import HighlightFeaturesHandler
from .events.identify_network_element_handler import IdentifyNetworkElementHandler
from .events.select_routesegments_handler import SelectRouteSegmentsHandler
from .events.user_error_occurred_handler import UserErrorOccurredHandler
import threading


class EventHandler:
    def __init__(self, iface, websocket, app_state):
        self.iface = iface
        self.websocket = websocket
        self.app_state = app_state
        self.geographicalAreaUpdatedHandler = GeographicalAreaUpdatedHandler(self.iface)
        self.getSelectedFeaturesHandler = RetrieveSelectedHandler(self.iface, self.websocket)
        self.panToCoordinateHandler = PanToCoordinateHandler(self.iface)
        self.highlightFeaturesHandler = HighlightFeaturesHandler(self.iface)
        self.identify_networkwork_element_handler = IdentifyNetworkElementHandler(self.websocket)
        self.select_routesegments_handler = SelectRouteSegmentsHandler(self.iface)
        self.user_error_occurred_handler = UserErrorOccurredHandler(self.iface)

    def handle(self, message):
        deserializedObject = self.deserialize(message);

        if deserializedObject.eventType == "ObjectsWithinGeographicalAreaUpdated":
            self.geographicalAreaUpdatedHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "RetrieveSelected":
            self.getSelectedFeaturesHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "PanToCoordinate":
            self.panToCoordinateHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "HighlightFeatures":
            self.highlightFeaturesHandler.handle(deserializedObject)
        elif deserializedObject.eventType == "RetrieveIdentifiedNetworkElement":
            self.identify_networkwork_element_handler.handle_message(self.app_state.last_identified_feature_mrid, self.app_state.last_identified_feature_type, deserializedObject)
        elif deserializedObject.eventType == "SelectRouteSegments":
            self.select_routesegments_handler.handle(deserializedObject)
        elif deserializedObject.eventType == "UserErrorOccurred":
            self.user_error_occurred_handler.handle(deserializedObject)

    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

from qgis.gui import QgsHighlight
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, QgsFeatureRequest
from ..application_settings import ApplicationSettings
import json
import time;

class HighlightFeaturesHandler:
    def __init__(self, iface):
        self.iface = iface

    def handle(self, message):
        route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_segment_name())[0]
        #route_node_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_node_name())[0]

        # The important part: get the feature iterator with an expression
        features = route_segment_layer.getFeatures(QgsFeatureRequest().setFilterExpression(u'"Counties" = \'Norwich\''))
        # Set the selection
        #route_segment_layer.setSelectedFeatures([f.id() for f in it])

        color = QColor(255, 0, 0)

        highlights = []
        for feature in features:
            identifyHighlight = QgsHighlight(self.iface.mapCanvas(), feature.geometry(), route_segment_layer)
            identifyHighlight.setWidth(3)
            identifyHighlight.setColor(color)
            highlights.append(identifyHighlight)

        for highlight in highlights:
            highlight.show()

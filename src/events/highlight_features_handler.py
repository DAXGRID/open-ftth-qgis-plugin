from qgis.gui import QgsHighlight
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, QgsFeatureRequest
from ..application_settings import ApplicationSettings
import json
import time;

class HighlightFeaturesHandler:
    def __init__(self, iface):
        self.iface = iface
        self.settings = ApplicationSettings()

    def handle(self, message):
        layer = None
        if message.featureType == self.settings.get_types_route_segment():
            layer = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_segment_name())[0]
        elif message.featureType == self.settings.get_types_route_node():
            layer = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_node_name())[0]

        filterExpression = ""
        for i in range(len(message.identifiedFeatureMrids)):
            mrid = message.identifiedFeatureMrids[i]
            if i == len(message.identifiedFeatureMrids) - 1:
                filterExpression += f'"mrid" = \'{mrid}\''
            else:
                filterExpression += f'"mrid" = \'{mrid}\' OR '

        features = layer.getFeatures(QgsFeatureRequest().setFilterExpression(filterExpression))

        color = QColor(0, 0, 255)
        highlightFeatures = []
        for feature in features:
            identifyHighlight = QgsHighlight(self.iface.mapCanvas(), feature.geometry(), layer)
            identifyHighlight.setWidth(3)
            identifyHighlight.setColor(color)
            highlightFeatures.append(identifyHighlight)

        for highlight in highlightFeatures:
            highlight.show()

        time.sleep(0.1) # Hack otherwise QGIS refresh bugs out
        self.iface.mapCanvas().refreshAllLayers()

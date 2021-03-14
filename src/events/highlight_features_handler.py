from qgis.gui import QgsHighlight
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, QgsFeatureRequest
from ..application_settings import ApplicationSettings
import getpass


class HighlightFeaturesHandler:
    def __init__(self, iface):
        self.iface = iface
        self.settings = ApplicationSettings()
        self.highlightFeatures = []

    def handle(self, message):
        if message.username != getpass.getuser():
            return

        for highlight in self.highlightFeatures:
            highlight.hide()

        self.highlightFeatures = []

        if len(message.identifiedFeatureMrids) == 0:
            return

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

        color = QColor(64, 224, 208)
        for feature in features:
            identifyHighlight = QgsHighlight(self.iface.mapCanvas(), feature.geometry(), layer)
            identifyHighlight.setWidth(5)
            identifyHighlight.setColor(color)
            self.highlightFeatures.append(identifyHighlight)

        for highlight in self.highlightFeatures:
            highlight.show()

        layer.triggerRepaint()

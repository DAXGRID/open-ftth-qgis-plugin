from qgis.gui import QgsHighlight
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, QgsFeatureRequest
from ..application_settings import ApplicationSettings


class SelectRouteSegmentsHandler:
    def __init__(self, iface):
        self.iface = iface
        self.settings = ApplicationSettings()
        self.highlightFeatures = []

    def handle(self, message):
        if message.username != self.settings.get_user_name_suffix():
            return

        layer = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_segment_name())[0]

        filterExpression = ""
        for i in range(len(message.mrids)):
            mrid = message.mrids[i]
            if i == len(message.mrids) - 1:
                filterExpression += f'"mrid" = \'{mrid}\''
            else:
                filterExpression += f'"mrid" = \'{mrid}\' OR '

        layer.selectByExpression(filterExpression)

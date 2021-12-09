from qgis.core import QgsProject
from qgis.core import QgsRectangle
from ..application_settings import ApplicationSettings


class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()

    def handle(self, message):
        minX = message.envelope.minX
        maxX = message.envelope.maxX
        minY = message.envelope.minY
        maxY = message.envelope.maxY

        extent = QgsRectangle(minX, minY, maxX, maxY)

        if self.iface.mapCanvas().extent().contains(extent):
            QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_segment_name())[0].triggerRepaint()
            QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_node_name())[0].triggerRepaint()

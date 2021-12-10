from qgis.core import QgsProject
from qgis.core import QgsRectangle
from ..application_settings import ApplicationSettings


class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()
        self.iface.mapCanvas().snappingUtils().setIndexingStrategy(self.iface.mapCanvas().snappingUtils().IndexingStrategy.IndexExtent)

    def handle(self, message):
        if not self.zoom_close_enough():
            return

        minX = message.envelope.minX
        maxX = message.envelope.maxX
        minY = message.envelope.minY
        maxY = message.envelope.maxY

        segmentLayer = QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_segment_name())[0]
        nodeLayer = QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_node_name())[0]

        extent = QgsRectangle(minX, minY, maxX, maxY)
        if self.iface.mapCanvas().extent().intersects(extent):
            # We only want to clear locators when the geoms changes.
            # This is because the clear locators are an expensive operation.
            if message.category == "RouteNetworkUpdated":
                segmentLayer.reload()
                nodeLayer.reload()
            else:
                segmentLayer.triggerRepaint()
                nodeLayer.triggerRepaint()

    def zoom_close_enough(self):
       return self.iface.mapCanvas().scale() < 1500

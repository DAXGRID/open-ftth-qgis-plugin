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

        segmentLayers = QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_segment_name())
        nodeLayers = QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_node_name())

        # In case that the layers are not loaded for the current project.
        if len(segmentLayers) != 1 or len(nodeLayers) != 1:
            return

        segmentLayer = segmentLayers[0]
        nodeLayer = nodeLayers[0]

        if self.inside_extent(message):
            # We only reload doing RouteNetworkUpdated message since this is an expensive operation
            if message.category == "RouteNetworkUpdated":
                segmentLayer.reload()
                nodeLayer.reload()
            else:
                segmentLayer.triggerRepaint()
                nodeLayer.triggerRepaint()

    def inside_extent(self, message):
        minX = message.envelope.minX
        maxX = message.envelope.maxX
        minY = message.envelope.minY
        maxY = message.envelope.maxY

        extent = QgsRectangle(minX, minY, maxX, maxY)

        return self.iface.mapCanvas().extent().intersects(extent)

    def zoom_close_enough(self):
       return self.iface.mapCanvas().scale() < 3000

from PyQt5.QtCore import QObject, pyqtSlot
from qgis.core import QgsVectorLayerCache, QgsProject
from qgis.gui import QgsVertexMarker, QgsMapCanvasSnappingUtils
from ..application_settings import ApplicationSettings

class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()

    def handle(self):
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_route_segment_layer_name())[0].triggerRepaint()
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_route_node_layer_name())[0].triggerRepaint()
        self.iface.mapCanvas().snappingUtils().clearAllLocators()

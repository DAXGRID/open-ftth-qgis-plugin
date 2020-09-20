from PyQt5.QtCore import QObject, pyqtSlot
from qgis.core import QgsVectorLayerCache, QgsProject
from qgis.gui import QgsVertexMarker, QgsMapCanvasSnappingUtils

class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface

    def handle(self):
        QgsProject.instance().mapLayersByName('route_segment')[0].triggerRepaint()
        QgsProject.instance().mapLayersByName('route_node')[0].triggerRepaint()
        self.iface.mapCanvas().snappingUtils().clearAllLocators()

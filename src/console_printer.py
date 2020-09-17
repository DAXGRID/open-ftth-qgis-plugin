from PyQt5.QtCore import QObject, pyqtSlot
from qgis.core import QgsVectorLayerCache, QgsProject
from qgis.gui import QgsVertexMarker, QgsMapCanvasSnappingUtils

class ConsolePrinter(QObject):
    def __init__(self, iface, parent=None):
        super(ConsolePrinter, self).__init__(parent)
        self.iface = iface;

    @pyqtSlot(str)
    def text(self, message):
        cachingEnabled = self.iface.mapCanvas().isCachingEnabled()

        QgsProject.instance().mapLayersByName('route_segment')[0].triggerRepaint()
        QgsProject.instance().mapLayersByName('route_node')[0].triggerRepaint()
        self.iface.mapCanvas().snappingUtils().clearAllLocators()

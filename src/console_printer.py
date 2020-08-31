from PyQt5.QtCore import QObject, pyqtSlot
from qgis.core import QgsVectorLayerCache
from qgis.gui import QgsVertexMarker, QgsMapCanvasSnappingUtils

class ConsolePrinter(QObject):
    def __init__(self, iface, parent=None):
        super(ConsolePrinter, self).__init__(parent)
        self.iface = iface;

    @pyqtSlot(str)
    def text(self, message):
        print (message)
        cachingEnabled = self.iface.mapCanvas().isCachingEnabled()

        for layer in self.iface.mapCanvas().layers():
            if cachingEnabled:
                layer.triggerRepaint()
                self.iface.mapCanvas().refresh()
                self.iface.mapCanvas().snappingUtils().clearAllLocators()

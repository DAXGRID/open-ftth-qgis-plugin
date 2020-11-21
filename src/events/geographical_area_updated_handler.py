from PyQt5.QtCore import QObject, pyqtSlot
from qgis.core import QgsVectorLayerCache, QgsProject
from qgis.gui import QgsVertexMarker, QgsMapCanvasSnappingUtils
from ..application_settings import ApplicationSettings
import time
import threading

class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()
        self.clearAllLocators = True
        self.semaphore = threading.Semaphore(1)

    def handle(self):
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_route_segment_layer_name())[0].triggerRepaint()
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_route_node_layer_name())[0].triggerRepaint()

        self.semaphore.acquire()

        if self.clearAllLocators:
            self.clearAllLocators = False
            threading.Thread(target = self.clearAllLocatorsTask).start()

        self.semaphore.release()

    def clearAllLocatorsTask(self):
        time.sleep(1) # Hack or QGIS crashes

        self.iface.mapCanvas().snappingUtils().clearAllLocators()
        self.clearAllLocators = True

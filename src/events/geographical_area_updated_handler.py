from qgis.core import QgsProject
from ..application_settings import ApplicationSettings
import time
import threading


class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()
        self.clearAllLocators = True

    def handle(self):
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_segment_name())[0].triggerRepaint()
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_node_name())[0].triggerRepaint()

        if self.clearAllLocators:
            self.clearAllLocators = False
            threading.Thread(target=self.clearAllLocatorsTask).start()

    def clearAllLocatorsTask(self):
        time.sleep(1)  # Hack or QGIS crashes

        self.iface.mapCanvas().snappingUtils().clearAllLocators()
        self.clearAllLocators = True

from qgis.core import QgsProject
from ..application_settings import ApplicationSettings



class GeographicalAreaUpdatedHandler:
    def __init__(self, iface):
        self.iface = iface
        self.applicationSettings = ApplicationSettings()

    def handle(self):
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_segment_name())[0].triggerRepaint()
        QgsProject.instance().mapLayersByName(self.applicationSettings.get_layers_route_node_name())[0].triggerRepaint()

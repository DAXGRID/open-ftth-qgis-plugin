from qgis.core import QgsProject
from qgis.core import Qgis
from ..application_settings import ApplicationSettings

class UserErrorOccurredHandler:
    def __init__(self, iface):
        self.iface = iface
        self.settings = ApplicationSettings()

    def handle(self, message):
        if message.username != self.settings.get_user_name_suffix():
            return

        self.iface.messageBar().pushMessage(
            "Error",
            message.errorCode,
            level=Qgis.Critical)

        # Reload RouteSegment and RouteNode layers after so no artifacts are left behind from rollback or delete.
        segmentLayers = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_segment_name())
        nodeLayers = QgsProject.instance().mapLayersByName(self.settings.get_layers_route_node_name())

        # In case that the layers are not loaded for the current project.
        if len(segmentLayers) != 1 or len(nodeLayers) != 1:
            QgsMessageLog.logMessage(
                "Could not find the route node or route segment layer doing refresh after user error occurred.",
                self.name,
                Qgis.Critical)
            return

        try:
            segmentLayers[0].reload()
            nodeLayers[0].reload()
        except TypeError as err:
            QgsMessageLog.logMessage(err, self.name, Qgis.Critical)
            self.iface.messageBar().pushMessage(
                "Error",
                "Could not reload layers, something went wrong doing refresh after user error occurred.",
                level=Qgis.Critical)

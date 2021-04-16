from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from qgis.core import QgsVectorLayer, QgsFeature, QgsPointXY, QgsProject
from qgis.gui import QgsMapToolIdentify
from .application_settings import ApplicationSettings


class IdentifySelect(QgsMapToolIdentify):
    identified = pyqtSignal(QgsVectorLayer, QgsFeature)
    identifiedNone = pyqtSignal()

    def __init__(self, canvas, layerType='AllLayers'):
        QgsMapToolIdentify.__init__(self, canvas)
        self.layerType = getattr(QgsMapToolIdentify, layerType)
        self.canvas = canvas
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.applicationSettings = ApplicationSettings()

    def canvasReleaseEvent(self, mouseEvent):
        layerNames = self.applicationSettings.get_layers_route_segment_name() + ', ' + self.applicationSettings.get_layers_route_node_name()
        layers = QgsProject.instance().mapLayersByName(layerNames)

        try:
            results = self.identify(mouseEvent.x(), mouseEvent.y(), layers)
        except Exception as e:
            print("Identify Exception: ", e)
            results = []

        if len(results) > 0:
            layer = results[0].mLayer
            self.identified.emit(layer, QgsFeature(results[0].mFeature))
        else:
            self.identifiedNone.emit()

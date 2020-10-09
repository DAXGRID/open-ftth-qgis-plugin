from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QCursor
from qgis.core import QgsVectorLayer, QgsFeature, QgsPointXY, QgsProject
from qgis.gui import QgsMapToolIdentify

class IdentifySelect(QgsMapToolIdentify):
    identified = pyqtSignal(QgsVectorLayer, QgsFeature)
    clicked = pyqtSignal(QgsPointXY)

    def __init__(self, canvas, layerType='AllLayers'):
        QgsMapToolIdentify.__init__(self, canvas)
        self.layerType = getattr(QgsMapToolIdentify, layerType)
        self.canvas = canvas
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def canvasReleaseEvent(self, mouseEvent):
        layers = QgsProject.instance().mapLayersByName('tree')

        try:
            results = self.identify(mouseEvent.x(), mouseEvent.y(), layers)
        except Exception as e:
            print("Identify Exception: ", e)
            results = []

        if len(results) > 0:
            layer = results[0].mLayer
            self.identified.emit(layer, QgsFeature(results[0].mFeature))
        else:
            self.clicked.emit(mouseEvent.originalMapPoint())

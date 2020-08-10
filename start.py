from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject

class Start:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('OPENFTTH', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.routeSegmentLayer = QgsProject.instance().mapLayersByName('route_segment')[0]
        self.routeSegmentLayer.layerModified.connect(self.logFeatureAdded)

        self.routeNodeLayer = QgsProject.instance().mapLayersByName('route_node')[0]
        self.routeNodeLayer.layerModified.connect(self.logFeatureAdded)

    def logFeatureAdded(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

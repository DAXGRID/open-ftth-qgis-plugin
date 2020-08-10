from PyQt5 import QtWidgets, QtGui;
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject
import os.path
from .resources import *
from .quick_edit_map_tool import QuickEditMapTool

class Start:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.setupActions()
        #self.map_canvas = self.iface.mapCanvas()
        #self.map_tool = QuickEditMapTool(self.map_canvas)

    def setupActions(self):
        icon_path = ':/plugins/open_ftth/icon.png'
        self.action = QAction(QtGui.QIcon(icon_path), "Open Ftth", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        self.route_segment_layer = QgsProject.instance().mapLayersByName('route_segment')[0]
        self.route_segment_layer.layerModified.connect(self.saveActiveLayerEdits)

        self.route_node_layer = QgsProject.instance().mapLayersByName('route_node')[0]
        self.route_node_layer.layerModified.connect(self.saveActiveLayerEdits)

    def saveActiveLayerEdits(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

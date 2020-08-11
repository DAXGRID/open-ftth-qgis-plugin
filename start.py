from PyQt5 import QtWidgets, QtGui;
from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.core import QgsVectorLayer, QgsProject
from .resources import *
from .quick_edit_map_tool import QuickEditMapTool

class Start:
    def __init__(self, iface):
        self.iface = iface
        self.map_canvas = self.iface.mapCanvas()
        self.map_tool = QuickEditMapTool(self.map_canvas)
        self.layer_modified_enabled = False;

    def initGui(self):
        self.setupActions()

    def setupActions(self):
        self.actions = []

        icon_path = ':/plugins/open_ftth/icon.png'
        self.action = QAction(QtGui.QIcon(icon_path), "Open Ftth", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.run)

        self.action_group = QtWidgets.QActionGroup(self.iface.mainWindow())
        self.action_group.addAction(self.action)

        self.actions.append(self.action)
        self.iface.addPluginToMenu("&Open Ftth", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        self.action.setChecked(False)
        self.layer_modified_enabled = False

    def run(self):
        if self.layer_modified_enabled is False:
            self.route_segment_layer = QgsProject.instance().mapLayersByName('route_segment')[0]
            self.route_segment_layer.layerModified.connect(self.saveActiveLayerEdits)

            self.route_node_layer = QgsProject.instance().mapLayersByName('route_node')[0]
            self.route_node_layer.layerModified.connect(self.saveActiveLayerEdits)

            self.layer_modified_enabled = True

    def saveActiveLayerEdits(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

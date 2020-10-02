from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtWebKit import QWebSettings
from qgis.PyQt.QtCore import Qt, QUrl
from qgis.core import QgsVectorLayer, QgsProject
from .resources import *
from .listen_websockets import ListenWebsocket
from .application_settings import ApplicationSettings
from .events.get_selected_features_handler import GetSelectedFeaturesHandler
import time
import asyncio

class Start:
    def __init__(self, iface):
        self.iface = iface
        self.autosave_enabled = False
        self.select_tool_enabled = False
        self.route_segment_layer = None
        self.route_node_layer = None
        self.websocket = ListenWebsocket(self.iface)
        self.websocket.start()

    def initGui(self):
        self.setupActions()

    def setupActions(self):
        self.actions = []

        icon_path = ":/plugins/open_ftth/icon.png"
        self.autosave_action = QAction(QtGui.QIcon(icon_path), "Autosave", self.iface.mainWindow())
        self.autosave_action.setCheckable(True)
        self.autosave_action.triggered.connect(self.setupAutoSave)

        self.select_action = QAction(QtGui.QIcon(icon_path), "Select", self.iface.mainWindow())
        self.select_action.triggered.connect(self.setupSelectTool);

        self.action_group = QtWidgets.QActionGroup(self.iface.mainWindow())
        self.action_group.addAction(self.autosave_action)
        self.action_group.addAction(self.select_action)
        self.action_group.setExclusive(False)

        self.actions.append(self.autosave_action)
        self.actions.append(self.select_action)

        self.iface.addPluginToMenu("&Open Ftth", self.autosave_action)
        self.iface.addToolBarIcon(self.autosave_action)
        self.iface.addToolBarIcon(self.select_action)

    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        self.autosave_action.setChecked(False)
        self.select_action.setChecked(False)

        self.autosave_enabled = False
        self.select_tool_enabled = False

        try:
            self.route_segment_layer.layerModified.disconnect()
            self.route_node_layer.layerModified.disconnect()
            self.websocket.onClose()
        except Exception:
            pass

    def setupSelectTool(self):
        selectedFeatures = GetSelectedFeaturesHandler(self.iface, self.websocket).handle()
        print(selectedFeatures)

    def setupAutoSave(self):
        if self.autosave_enabled is False:
            self.route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_route_segment_layer_name())[0]
            self.route_segment_layer.layerModified.connect(self.saveActiveLayerEdits)

            self.route_node_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_route_node_layer_name())[0]
            self.route_node_layer.layerModified.connect(self.saveActiveLayerEdits)

            self.autosave_enabled = True
            self.saveActiveLayerEdits()

        else:
            self.route_segment_layer.layerModified.disconnect()
            self.route_node_layer.layerModified.disconnect()
            self.autosave_action.setChecked(False)
            self.autosave_enabled = False

    def saveActiveLayerEdits(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

    def onIdentified(self, selected_layer, selected_feature):
        selected_layer.removeSelection()
        selected_layer.select(selected_feature.id())

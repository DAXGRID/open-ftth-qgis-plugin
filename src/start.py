from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction, QMessageBox, QActionGroup, QWidgetAction
from PyQt5.QtGui import QCursor
from PyQt5.QtWebKit import QWebSettings
from qgis.PyQt.QtCore import Qt, QUrl
from qgis.core import QgsVectorLayer, QgsProject
from qgis.gui import QgsMapCanvas
from .resources import *
from .listen_websockets import ListenWebsocket
from .application_settings import ApplicationSettings
from .events.get_selected_features_handler import GetSelectedFeaturesHandler
from .identify_select import IdentifySelect
import time
import asyncio

class Start:
    def __init__(self, iface):
        self.iface = iface
        self.autosave_enabled = False
        self.route_segment_layer = None
        self.route_node_layer = None
        self.websocket = ListenWebsocket(self.iface)
        self.websocket.start()
        self.getSelectedFeaturesHandler = GetSelectedFeaturesHandler(self.iface, self.websocket)

    def initGui(self):
        self.setupActions()

    def setupActions(self):
        self.actions = []

        icon_auto_save = ":/plugins/open_ftth/auto_save.svg"
        auto_identify = ":/plugins/open_ftth/auto_identify.svg"
        self.autosave_action = QAction(QtGui.QIcon(icon_auto_save), "Autosave", self.iface.mainWindow())
        self.autosave_action.setCheckable(True)
        self.autosave_action.triggered.connect(self.setupAutoSave)

        self.select_action = QAction(QtGui.QIcon(auto_identify), "Select", self.iface.mainWindow())
        self.select_action.setCheckable(True)
        self.select_action.triggered.connect(self.setupSelectTool);

        self.iface.addPluginToMenu("&OPEN FTTH", self.select_action)
        self.iface.addToolBarIcon(self.autosave_action)
        self.iface.addToolBarIcon(self.select_action)

        self.identify_tool = IdentifySelect(self.iface.mapCanvas())
        self.identify_tool.identified.connect(self.onIdentified)

        # Build an action list from QGIS navigation toolbar
        actionList = self.iface.mapNavToolToolBar().actions()

        # Add actions from QGIS attributes toolbar (handling QWidgetActions)
        tmpActionList = self.iface.attributesToolBar().actions()        
        for action in tmpActionList:
            if isinstance(action, QWidgetAction):
                actionList.extend( action.defaultWidget().actions()) 
            else:
                actionList.append(action) 

         # ... add other toolbars' action lists...
        tmpActionList = self.iface.digitizeToolBar().actions()        
        for action in tmpActionList:
            if isinstance(action, QWidgetAction):
                actionList.extend(action.defaultWidget().actions())
            else:
                actionList.append(action) 

         # Build a group with actions from actionList and add your own action
        group = QActionGroup(self.iface.mainWindow())
        group.setExclusive(True)
        for action in actionList:
            group.addAction(action)
        group.addAction(self.select_action)

    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)

        self.autosave_action.setChecked(False)
        self.select_action.setChecked(False)

        self.autosave_enabled = False
        self.select_tool_enabled = False

        try:
            self.disconnectSelectedFeatures()
            self.disconnectSelectTool()
            self.websocket.close()
        except Exception:
            pass

    def setupSelectTool(self):
        self.iface.mapCanvas().setMapTool(self.identify_tool)

    def sendSelectedFeatures(self):
        self.getSelectedFeaturesHandler.handle()

    def setupAutoSave(self):
        if self.autosave_enabled is False:
            self.connectAutosave()
            self.saveActiveLayerEdits()
        else:
            self.disconnectAutosave()

    def connectAutosave(self):
        self.route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_route_segment_layer_name())[0]
        self.route_segment_layer.layerModified.connect(self.saveActiveLayerEdits)

        self.route_node_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_route_node_layer_name())[0]
        self.route_node_layer.layerModified.connect(self.saveActiveLayerEdits)

        self.autosave_enabled = True

    def disconnectAutosave(self):
        self.route_segment_layer.layerModified.disconnect(self.saveActiveLayerEdits)
        self.route_node_layer.layerModified.disconnect(self.saveActiveLayerEdits)
        self.autosave_action.setChecked(False)
        self.autosave_enabled = False

    def saveActiveLayerEdits(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

    def onIdentified(self, selected_layer, selected_feature):
        print(selected_feature.id())
        selected_layer.removeSelection()
        selected_layer.select(selected_feature.id())

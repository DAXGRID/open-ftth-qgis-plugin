from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QActionGroup, QWidgetAction, QApplication
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, Qgis, QgsFeatureRequest, QgsVectorLayerUndoCommandDeleteFeature, QgsMessageLog, QgsGeometry
from qgis.gui import QgsHighlight, QgsMessageBar
from io import StringIO

from .resources import *
from .bridge_websocket import BridgeWebsocket
from .application_settings import ApplicationSettings
from .identify_select import IdentifySelect
from .events.identify_network_element_handler import IdentifyNetworkElementHandler
from .events.retrieve_selected_handler import RetrieveSelectedHandler
from .event_handler import EventHandler

import webbrowser
import sys
import csv


class Start:
    def __init__(self, iface):
        self.name = "OPEN_FTTH"
        self.iface = iface
        self.autosave_enabled = False
        self.route_segment_layer = None
        self.route_node_layer = None
        self.websocket = BridgeWebsocket(self.iface)

        self.identifyHighlight = None
        self.last_identified_feature_mrid = None
        self.last_identified_feature_type = None

        self.event_handler = EventHandler(self.iface, self.websocket.websocket, self)
        self.websocket.messageReceived.connect(self.event_handler.handle)

        self.identifyNetworkElementHandler = IdentifyNetworkElementHandler(self.websocket)
        self.retrieve_selected_handler = RetrieveSelectedHandler(self.iface, self.websocket)
        self.application_settings = ApplicationSettings()
        self.layers_loaded = False

    def initGui(self):
        self.setupActions()
        self.iface.layerTreeView().currentLayerChanged.connect(self.layersLoaded)
        self.iface.layerTreeView().currentLayerChanged.connect(self.layerSelectionChange)

    def setupActions(self):
        self.actions = []

        icon_auto_save = ":/plugins/open_ftth/auto_save.svg"
        self.autosave_action = QAction(QtGui.QIcon(icon_auto_save), "Autosave", self.iface.mainWindow())
        self.autosave_action.setCheckable(True)
        self.autosave_action.triggered.connect(self.setupAutoSave)

        auto_identify = ":/plugins/open_ftth/auto_identify.svg"
        self.select_action = QAction(QtGui.QIcon(auto_identify), "Select", self.iface.mainWindow())
        self.select_action.setCheckable(True)
        self.select_action.triggered.connect(self.setupSelectTool);

        web_browser = ":/plugins/open_ftth/browser_icon.svg"
        self.web_browser_action = QAction(QtGui.QIcon(web_browser), "Web-browser", self.iface.mainWindow())
        self.web_browser_action.setCheckable(False)
        self.web_browser_action.triggered.connect(self.connectWebBrowser)

        copy_geometry = ":/plugins/open_ftth/copy_geometry.svg"
        self.copy_geometry_action = QAction(QtGui.QIcon(copy_geometry), "Copy geometry", self.iface.mainWindow())
        self.copy_geometry_action.setCheckable(False)
        self.copy_geometry_action.triggered.connect(self.pasteGeometry)

        self.iface.addPluginToMenu("&OPEN FTTH", self.select_action)
        self.iface.addToolBarIcon(self.autosave_action)
        self.iface.addToolBarIcon(self.select_action)
        self.iface.addToolBarIcon(self.web_browser_action)
        self.iface.addToolBarIcon(self.copy_geometry_action);

        self.identify_tool = IdentifySelect(self.iface.mapCanvas())
        self.identify_tool.identified.connect(self.onIdentified)
        self.identify_tool.identifiedNone.connect(self.onIdentifiedNone)
        self.buildActionListIdentifyTool()

    def buildActionListIdentifyTool(self):
        actionList = self.iface.mapNavToolToolBar().actions()

        # Add actions from QGIS attributes toolbar (handling QWidgetActions)
        tmpActionList = self.iface.attributesToolBar().actions()
        for action in tmpActionList:
            if isinstance(action, QWidgetAction):
                actionList.extend(action.defaultWidget().actions())
            else:
                actionList.append(action)

        tmpActionList = self.iface.digitizeToolBar().actions()
        for action in tmpActionList:
            if isinstance(action, QWidgetAction):
                actionList.extend(action.defaultWidget().actions())
            else:
                actionList.append(action)

        tmpActionList = self.iface.selectionToolBar().actions()
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
            self.route_segment_layer.beforeCommitChanges.disconnect(self.preCommitDeleteHandlerRouteSegment)
            self.route_node_layer.beforeCommitChanges.disconnect(self.preCommitDeleteHandlerRouteNode)
            self.route_node_layer.featuresDeleted.disconnect(self.checkFeaturesDeleted)
            self.route_segment_layer.featuresDeleted.disconnect(self.checkFeaturesDeleted)
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

    def layersLoaded(self):
        if not self.hasCorrectLayers():
            self.onIdentifiedNone()
            return

        if self.layers_loaded is False:
            self.websocket.start()
            self.layers_loaded = True
            self.route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_segment_name())[0]
            self.route_node_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_node_name())[0]

            try:
                self.route_node_layer.featuresDeleted.connect(self.checkFeaturesDeleted)
                self.route_segment_layer.featuresDeleted.connect(self.checkFeaturesDeleted)
            except TypeError:
                pass

            try:
                self.route_segment_layer.beforeCommitChanges.connect(self.preCommitDeleteHandlerRouteSegment)
                self.route_node_layer.beforeCommitChanges.connect(self.preCommitDeleteHandlerRouteNode)
            except TypeError:
                pass

    def layerSelectionChange(self):
        if not self.hasCorrectLayers():
            self.onIdentifiedNone()
            return

        self.route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_segment_name())[0]
        try:
            self.route_segment_layer.selectionChanged.disconnect(self.onSelectedSegment)
        except TypeError:
            pass

        self.route_segment_layer.selectionChanged.connect(self.onSelectedSegment)

    def hasCorrectLayers(self):
        route_segment_layers = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_segment_name())
        route_node_layers = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_node_name())
        return len(route_segment_layers) > 0 and len(route_node_layers) > 0

    def connectAutosave(self):
        # We do this to avoid plugin crash in case that connects come in an invalid state.
        try:
            self.route_segment_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_segment_name())[0]
            self.route_segment_layer.layerModified.connect(self.saveActiveLayerEdits)
        except TypeError:
            pass

        # We do this to avoid plugin crash in case that connects come in an invalid state.
        try:
            self.route_node_layer = QgsProject.instance().mapLayersByName(ApplicationSettings().get_layers_route_node_name())[0]
            self.route_node_layer.layerModified.connect(self.saveActiveLayerEdits)
        except TypeError:
            pass

        self.autosave_enabled = True

    def disconnectAutosave(self):
        # We do this to avoid plugin crash in case that connects come in an invalid state.
        try:
            self.route_segment_layer.layerModified.disconnect(self.saveActiveLayerEdits)
        except TypeError:
            pass

        # We do this to avoid plugin crash in case that connects come in an invalid state.
        try:
            self.route_node_layer.layerModified.disconnect(self.saveActiveLayerEdits)
        except TypeError:
            pass

        self.autosave_action.setChecked(False)
        self.autosave_enabled = False

    def connectWebBrowser(self):
        webbrowser.open(self.application_settings.get_website_url(), new=2)

    def saveActiveLayerEdits(self):
        self.iface.actionSaveActiveLayerEdits().trigger()

    def onSelectedSegment(self):
        message = type('Expando', (object,), {'username': self.application_settings.get_user_name_prefix()})()
        self.retrieve_selected_handler.handle(message)

    def checkFeaturesDeleted(self, fids):
        if self.last_identified_feature_mrid is None:
            return

        features = None
        filterExpression = f'"mrid" = \'{self.last_identified_feature_mrid}\''
        if self.last_identified_feature_type == self.application_settings.get_types_route_node():
            features = self.route_node_layer.getFeatures(QgsFeatureRequest().setFilterExpression(filterExpression))
        elif self.last_identified_feature_type == self.application_settings.get_types_route_segment():
            features = self.route_segment_layer.getFeatures(QgsFeatureRequest().setFilterExpression(filterExpression))
        else:
            return

        # hack because the deleted signal is triggered on both create and delete
        stillExists = False
        for feature in features:
            stillExists = True

        if not stillExists:
            self.onIdentifiedNone()
            self.identifyNetworkElementHandler.handle(None, None)
        # end of hack

    def onIdentified(self, selected_layer, selected_feature):
        selected_type = ""
        if self.application_settings.get_layers_route_node_name() == selected_layer.sourceName():
            selected_type = self.application_settings.get_types_route_node()
        elif self.application_settings.get_layers_route_segment_name() == selected_layer.sourceName():
            selected_type = self.application_settings.get_types_route_segment()
        else:
            self.identifyHighlight.hide()
            return

        if self.identifyHighlight is not None:
            self.identifyHighlight.hide()

        color = QColor(0, 255, 0)
        self.identifyHighlight = QgsHighlight(self.iface.mapCanvas(), selected_feature.geometry(), selected_layer)
        self.identifyHighlight.setWidth(3)
        self.identifyHighlight.setColor(color)
        self.identifyHighlight.show()

        mrid = selected_feature.attribute("mrid")

        self.last_identified_feature_mrid = mrid
        self.last_identified_feature_type = selected_type

        if selected_type != "":
            self.identifyNetworkElementHandler.handle(mrid, selected_type)

    def onIdentifiedNone(self):
        if self.identifyHighlight is not None:
            self.last_identified_feature_mrid = None
            self.last_identified_feature_type = None
            self.identifyHighlight.hide();

    def preCommitDeleteHandlerRouteSegment(self):
        self.undoDeleteSetMarkedToBeDeleted(ApplicationSettings().get_layers_route_segment_name())

    def preCommitDeleteHandlerRouteNode(self):
        self.undoDeleteSetMarkedToBeDeleted(ApplicationSettings().get_layers_route_node_name())

    def undoDeleteSetMarkedToBeDeleted(self, layerName):
        layers = QgsProject.instance().mapLayersByName(layerName)
        if len(layers) != 1:
            return
        layer = layers[0]

        deleted_features_ids = layer.editBuffer().deletedFeatureIds()
        for feature_id in deleted_features_ids:
            QgsVectorLayerUndoCommandDeleteFeature(layer.editBuffer(), feature_id).undo()

        marked_to_be_deleted_idx = layer.fields().indexOf('marked_to_be_deleted')
        user_name_idx = layer.fields().indexOf('user_name')
        user_name = self.application_settings.get_user_name()
        for feature in layer.dataProvider().getFeatures(QgsFeatureRequest().setFilterFids(deleted_features_ids)):
            layer.changeAttributeValue(feature.id(), marked_to_be_deleted_idx, True)
            layer.changeAttributeValue(feature.id(), user_name_idx, user_name)

    def pasteGeometry(self):
        layer = self.iface.activeLayer()
        if not layer.isEditable():
            self.showBarMessage("You need to be in edit mode to paste the geometry.", Qgis.Warning)
            return

        geoms = self.tryGetFeaturesGeomsFromClipBoard()
        if len(geoms) > 1:
            self.showBarMessage("Can't paste geometry multiple features in clipboard.", Qgis.Warning)
            return

        if len(geoms) == 0:
            self.showBarMessage("Can't paste geometry. No features in clipboard.", Qgis.Warning)
            return

        selected_features = layer.selectedFeatures()

        if len(selected_features) == 0:
            self.showBarMessage("Can't paste. No target feature to paste to.", Qgis.Warning)
            return

        paste_feature = selected_features[0]
        paste_geom = paste_feature.geometry()
        copy_geom = geoms[0]

        if paste_geom.type() != copy_geom.type():
            self.showBarMessage("Not the same geometry type. From %s to %s" % (copy_geom.type(), paste_geom.type()), Qgis.Warning)
            return

        paste_geom_start = paste_geom.asPolyline()[0]
        copy_geom_start = copy_geom.asPolyline()[0]
        copy_geom_end = copy_geom.asPolyline()[len(copy_geom.asPolyline()) - 1]

        start_to_start_distance = paste_geom_start.distance(copy_geom_start)
        start_to_end_distance = paste_geom_start.distance(copy_geom_end)

        new_copy_geom = copy_geom.asPolyline()

        if start_to_start_distance > start_to_end_distance:
            # Then we reverse the geometry
            QgsMessageLog.logMessage("The geometries are flipped, we reverse them for the copy.", self.name, Qgis.Info)
            new_copy_geom.reverse()

        result = layer.changeGeometry(paste_feature.id(), QgsGeometry.fromPolylineXY(new_copy_geom))

        if not result:
            self.showBarMessage("Can't paste geometry, something went wrong.", Qgis.Critical)
            return

        self.iface.mapCanvas().refresh()

    def tryGetFeaturesGeomsFromClipBoard(self):
        cb = QApplication.clipboard()
        clipboard_text = cb.text()
        if sys.version_info[0] == 2:
            clipboard_text = clipboard_text.encode('utf-8')

        reader = csv.DictReader(
            StringIO(clipboard_text),
            delimiter='\t'
        )

        geoms = []
        for row in reader:
            wkt_geom = row.get('wkt_geom')
            geom = QgsGeometry.fromWkt(wkt_geom)

            if not geom:
                self.showBarMessage('Can\'t create geometry from wkt: %s' % wkt_geom, Qgis.Critical)
                return []

            geoms.append(geom)
        return geoms

    def showBarMessage(self, message, level=Qgis.Info, duration=-1):
        self.iface.messageBar().pushMessage("Error", message, level=level, duration=duration)

from qgis.core import QgsRectangle
from ..application_settings import ApplicationSettings
import time


class PanToCoordinateHandler:
    def __init__(self, iface):
        self.iface = iface
        self.settings = ApplicationSettings()

    def handle(self, message):
        if message.username != self.settings.get_user_name_prefix():
            return

        x = message.coordinate[0]
        y = message.coordinate[1]

        canvas = self.iface.mapCanvas()
        currExt = canvas.extent()

        canvasCenter = currExt.center()
        dx = float(x) - canvasCenter.x()
        dy = float(y) - canvasCenter.y()

        xMin = currExt.xMinimum() + dx
        xMax = currExt.xMaximum() + dx
        yMin = currExt.yMinimum() + dy
        yMax = currExt.yMaximum() + dy

        newRect = QgsRectangle(xMin, yMin, xMax, yMax)
        canvas.setExtent(newRect)
        time.sleep(0.1)  # Hack otherwise QGIS refresh bugs out
        canvas.refreshAllLayers()

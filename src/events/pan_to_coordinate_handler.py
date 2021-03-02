import getpass
from qgis.core import QgsRectangle
import time


class PanToCoordinateHandler:
    def __init__(self, iface):
        self.iface = iface

    def handle(self, message):
        if message.username != getpass.getuser():
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

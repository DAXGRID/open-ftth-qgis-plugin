from qgis.PyQt import QtCore
from .event_handler import EventHandler
from .application_settings import ApplicationSettings
from .libs import websocket
import time


class BridgeWebsocket(QtCore.QThread):
    def __init__(self, iface, parent=None):
        super(BridgeWebsocket, self).__init__(parent)
        self.iface = iface
        self.retries = 0

        websocket.enableTrace(True)

        self.websocket = websocket.WebSocketApp(ApplicationSettings().get_websocket_url(),
                                on_message = lambda ws,msg: self.onMessage(ws, msg),
                                on_error = lambda ws,msg: self.onError(ws, msg),
                                on_open = lambda ws: self.onOpen(ws))

        self.eventHandler = EventHandler(self.iface, self.websocket)

    def run(self):
        self.websocket.run_forever()

    def onOpen(self, ws):
        print("Connected")
        self.retries = 0

    def onMessage(self, ws, message):
        self.eventHandler.handle(message)

    def onError(self, ws, error):
        print(error)
        print("Reconnecting to WS")
        self.reconnect()

    def reconnect(self):
        self.websocket.close()
        if self.retries >= 10:
            print("Waiting 60 secs before trying to reconnect")
            time.sleep(60)
            self.retries = 0
        else:
            time.sleep(3)
            self.retries += 1

        self.run()

    def onClose(self, ws):
        print("Connected closed")

    def send(self, message):
        self.websocket.send(message)

    def close(self):
        self.websocket.close()

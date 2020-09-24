from qgis.PyQt import QtCore
from .event_handler import EventHandler
import websocket
import _thread as thread
import time;

class ListenWebsocket(QtCore.QThread):
    def __init__(self, iface, parent=None):
        super(ListenWebsocket, self).__init__(parent)
        self.iface = iface;

        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp("ws://localhost:5000/ws",
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error = lambda ws,msg: self.on_error(ws, msg),
                                on_open = lambda ws: self.on_open(ws)) 

    def run(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        EventHandler(self.iface).handle(message)

    def on_error(self, ws, error):
        print(error)
        self.reconnect()
       
    def reconnect(self):
        self.ws.close();
        time.sleep(3)
        self.run() 

    def on_close(self, ws):
        print("### closed ###")

    def send(self, message):
        self.ws.send(message)

    def close(self):
        self.ws.close()

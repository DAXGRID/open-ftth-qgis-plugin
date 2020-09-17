from qgis.PyQt import QtCore
import websocket
import _thread as thread
import time;

class ListenWebsocket(QtCore.QThread):
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)

        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp("ws://localhost:5000/ws",
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error = lambda ws,msg: self.on_error(ws, msg),
                                on_close = lambda ws: self.on_close(ws),
                                on_open = lambda ws: self.on_open(ws)) 

    def run(self):
        self.ws.run_forever()

    def on_open(self, ws):
        def run(*args):
            for i in range(10000):
                time.sleep(0.1)
                ws.send("Hello %d" % i)
            time.sleep(0.1)
            ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())


    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def send(self, message):
        self.ws.send(message)

    def close(self):
        self.ws.close()

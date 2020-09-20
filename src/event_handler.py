import json
import base64
from types import SimpleNamespace

class EventHandler:
    def handle(self, message):
        json = base64.b64decode(message);
        deserializedObject = self.deserialize(json);
        print(deserializedObject.eventType)
        
    def deserialize(self, jsonMessage):
        return json.loads(jsonMessage, object_hook=lambda d: SimpleNamespace(**d))

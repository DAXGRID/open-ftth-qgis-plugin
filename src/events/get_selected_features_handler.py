class GetSelectedFeaturesHandler:
    def __init__(self, iface):
        self.iface = iface

    def handle(self):
        return self.iface.mapCanvas().currentLayer().selectedFeatures()

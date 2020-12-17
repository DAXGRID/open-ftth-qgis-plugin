import os
from configparser import ConfigParser 

class ApplicationSettings:
    def __init__(self):
        self.configuration = ConfigParser()
        self.configuration.read(os.path.dirname(__file__) + '/config.ini')

    def get_websocket_url(self):
        return self.configuration.get("websocket", "url")

    def get_route_segment_layer_name(self):
        return self.configuration.get('layers', "routesegment")

    def get_route_node_layer_name(self):
        return self.configuration.get('layers', "routenode")

    def get_website_url(self):
        return self.configuration.get('website', 'url')

    def get_types_route_segment(self):
        return self.configuration.get('types', 'routesegment')

    def get_types_route_node(self):
        return self.configuration.get('types', 'routenode')

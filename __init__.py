def classFactory(iface):
    """Load OpenFtth class from file OpenFtth.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .open_ftth import OpenFtth
    return OpenFtth(iface)

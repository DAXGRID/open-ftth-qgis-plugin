# OpenFTTH - QGIS Plugin

This plugin is an integral part of the full OpenFTTH system and requires the system to function. Its primary purpose is to facilitate communication with the OpenFTTH system.

As the system is currently being developed, there is not yet a large amount of documentation available. However, if you have any questions or would like to learn more, please feel free to reach out to us.

## Dependencies

```bash
pip install pyqt5
```

## To update icons

```sh
pyrcc5 -o resources.py ./src/resources/resources.qrc
```

## Install

Install by copying the entire directory to:

```sh
/{myhomepath}/.local/share/QGIS/QGIS3/profiles/default/python/plugins
```

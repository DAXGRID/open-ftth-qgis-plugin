# Open Ftth - QGIS Plugin

Open Ftth Plugin for QGIS (Currently under development)

## Note

* This plugin is part of the full OpenFTTH system, to work it requires that system to run. It's only purpose is to communicate with the OpenFTTH system, therefore not a lot of functionality is built into the plugin.

## Dependencies

```bash
pip install pyqt5
```

## To update icons

```sh
pyrcc5 -o resources.py resources/resources.qrc
```

## Install

Install by copying the entire directory to:

```sh
/{myhomepath}/.local/share/QGIS/QGIS3/profiles/default/python/plugins
```

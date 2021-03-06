# Open Ftth - QGIS Plugin

Open Ftth Plugin for QGIS (Currently under development)

## Information

* This plugin is part of the full OpenFTTH system, to work it requires that system to run. It's only purpose is to communicate with the OpenFTTH system, therefore not a lot of functionality is built into the plugin.

For now you can check the overview - some of it is outdated [link](https://github.com/DAXGRID/open-ftth-overview), but in the future a webpage will be made with an overview of the system.

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

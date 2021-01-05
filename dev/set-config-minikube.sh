#!/usr/bin/env bash

DESKTOP_BRIDGE_HOST=$(minikube ip)
DESKTOP_BRIDGE_PORT=$(kubectl describe service openftth-desktop-bridge -n openftth | grep NodePort -m 1 | grep -o '[0-9]\+')

WEBSITE_HOST=$(minikube ip)
WEBSITE_PORT=$(kubectl describe service openftth-frontend -n openftth | grep NodePort -m 1 | grep -o '[0-9]\+')

sed -i "s/url = ws:.*/url = ws:\/\/$DESKTOP_BRIDGE_HOST:$DESKTOP_BRIDGE_PORT\/ws/" src/config.ini
sed -i "s/url = http:.*/url = http:\/\/$WEBSITE_HOST:$WEBSITE_PORT/" src/config.ini

#!/bin/bash

python3 websocket_server.py &
echo "WS Server Started"
waitress-serve app:app
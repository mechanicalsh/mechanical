#!/bin/bash
export ACCEPT_EULA=Y PRIVACY_CONSENT=Y OMNI_KIT_ACCEPT_EULA=YES NVIDIA_DRIVER_CAPABILITIES=all
echo "[onstart] installing deps" > /root/onstart.log
/isaac-sim/python.sh -m pip install -q Pillow aiohttp >> /root/onstart.log 2>&1
echo "[onstart] fetching stream_server.py" >> /root/onstart.log
curl -sL "https://gist.githubusercontent.com/roboalias/371d3b2e7b6dd64cd2f5bd58d05c432d/raw/stream_server.py" -o /root/stream_server.py
echo "[onstart] launching stream" >> /root/onstart.log
/isaac-sim/python.sh /root/stream_server.py >> /root/stream.log 2>&1
echo "[onstart] stream exited" >> /root/onstart.log
sleep infinity

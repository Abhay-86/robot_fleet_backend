import zenoh
import json
import time


config = zenoh.Config()

config.insert_json5(
    "connect/endpoints",
    '["tcp/127.0.0.1:7447"]'
)

session = zenoh.open(config)

time.sleep(1)

session.put(
    "robots/r1/cmd",
    json.dumps({
        "cmd": "w"
    })
)

print("Command sent")

time.sleep(2)

session.close()
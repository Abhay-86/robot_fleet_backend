import json
import zenoh


config = zenoh.Config()

config.insert_json5(
    "connect/endpoints",
    '["tcp/127.0.0.1:7447"]'
)

session = zenoh.open(config)


def send_robot_command(
    robot_id,
    cmd,
    value=None
):

    payload = {
        "cmd": cmd
    }

    if value is not None:
        payload["value"] = value

    session.put(
        f"robots/{robot_id}/cmd",
        json.dumps(payload)
    )
import asyncio
from bleak import BleakClient
from pydantic import BaseModel
from typing import Literal
import argparse


class OctahedronOrientationChangeEvent(BaseModel):
    """
    The octahedron sends events every time it detects that its orientation changed.

    Change events are only emitted once the tracker has been idle for a bit.

    The change event always contains the number of the face or vertex that was detected as being 'on top' at the time when the change was emitted.
    By 'top face/vertex', we mean specifically:
    - the one with the 'highest vertical coordinate' or, equivalently
    - the one with the 'largest distance from the ground'

    Therefore, there are only two types of possible changes that are emitted:
     - `face` if the octahedron's 'top face' changed or
     - `vertex` if the octahedron's 'top vertex' changed

    To be specific:
    - for `change_type="face"`, the number of the octahedron's 'top face' is emitted as `number` (and, as a consequence, we can assume that the octahedron lies on the face which is on the _opposite_ side of that face)
    - for `change_type="vertex"`, the number of the octahedron's 'top vertex' is emitted as `number` (and, as a consequence, we can assume that the octahedron 'stands' on the vertex which is on the _opposite_ side of that vertex; in practical terms, it means that the octahdron is placed in its 'base')
    """

    change_type: Literal["face", "vertex"]
    number: int


# Standard BLE SIG UUIDs
BATTERY_LEVEL_CHAR = "00002a19-0000-1000-8000-00805f9b34fb"
BATTERY_POWER_STATE_CHAR = "00002a1a-0000-1000-8000-00805f9b34fb"

MANUFACTURER_NAME_CHAR = "00002a29-0000-1000-8000-00805f9b34fb"
MODEL_NUMBER_CHAR = "00002a24-0000-1000-8000-00805f9b34fb"
FIRMWARE_REVISION_CHAR = "00002a26-0000-1000-8000-00805f9b34fb"
HARDWARE_REVISION_CHAR = "00002a27-0000-1000-8000-00805f9b34fb"
SOFTWARE_REVISION_CHAR = "00002a28-0000-1000-8000-00805f9b34fb"


async def read_str(client: BleakClient, uuid: str) -> str | None:
    try:
        data = await client.read_gatt_char(uuid)
        return data.decode("utf-8").strip()
    except Exception:
        return None


async def read_byte(client: BleakClient, uuid: str) -> int | None:
    try:
        data = await client.read_gatt_char(uuid)
        return data[0]
    except Exception:
        return None


async def get_device_info(client: BleakClient):
    print("=== Device Information ===")
    print(f"Manufacturer : {await read_str(client, MANUFACTURER_NAME_CHAR)}")
    print(f"Model        : {await read_str(client, MODEL_NUMBER_CHAR)}")
    print(f"Firmware     : {await read_str(client, FIRMWARE_REVISION_CHAR)}")
    print(f"Hardware     : {await read_str(client, HARDWARE_REVISION_CHAR)}")
    print(f"Software     : {await read_str(client, SOFTWARE_REVISION_CHAR)}")

    print("\n=== Battery ===")
    level = await read_byte(client, BATTERY_LEVEL_CHAR)
    print(f"Level        : {level}%")

    state = await read_byte(client, BATTERY_POWER_STATE_CHAR)
    if state is not None:
        # 0x00 = not charging, 0x02 = charging (tested on device w/ LightBlue app)
        charging = state == 0x02
        print(f"Charging     : {'yes' if charging else 'no'}")


ORIENTATION_CHAR = "c7e70012-c847-11e6-8175-8c89a55d403c"
"""UUID of Timeular's orientation GATT characteristic (reverse-engineered from BLE sniffing)"""


NUMBER_TO_EVENT: dict[int, OctahedronOrientationChangeEvent] = {
    # adjacent to faces 1-4
    0: OctahedronOrientationChangeEvent(change_type="vertex", number=0),
    1: OctahedronOrientationChangeEvent(change_type="face", number=1),
    2: OctahedronOrientationChangeEvent(change_type="face", number=2),
    3: OctahedronOrientationChangeEvent(change_type="face", number=3),
    4: OctahedronOrientationChangeEvent(change_type="face", number=4),
    5: OctahedronOrientationChangeEvent(change_type="face", number=5),
    6: OctahedronOrientationChangeEvent(change_type="face", number=6),
    7: OctahedronOrientationChangeEvent(change_type="face", number=7),
    8: OctahedronOrientationChangeEvent(change_type="face", number=8),
    9: OctahedronOrientationChangeEvent(change_type="vertex", number=9),
    10: OctahedronOrientationChangeEvent(change_type="vertex", number=10),
    11: OctahedronOrientationChangeEvent(change_type="vertex", number=11),
    12: OctahedronOrientationChangeEvent(change_type="vertex", number=12),
    13: OctahedronOrientationChangeEvent(change_type="vertex", number=13),
    14: OctahedronOrientationChangeEvent(change_type="vertex", number=14),
}
"""
The octahedron sends simple numbers to indicate what kind of change was detected.

This dictionary maps the numbers to actual useable events.
"""


def on_orientation(sender, data: bytearray):
    event_idx = data[0]
    event = NUMBER_TO_EVENT.get(event_idx)
    if event is None:
        # shouldn't really happen afaik, but just in case...
        print(f"Unknown event: {event_idx}")
        return

    print(event)


async def read_octahedron(device_address: str):
    async with BleakClient(device_address) as client:
        print(
            "Connected to device" if client.is_connected else "Disconnected from device"
        )
        await get_device_info(client)

        await client.start_notify(ORIENTATION_CHAR, on_orientation)
        print("Listening for orientation changes... (Ctrl+C to stop)")
        await asyncio.sleep(3600)  # listen for 1 hour


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "device_address",
        type=str,
        help="The address of the octahedron (officially sold as 'Time Tracking Cube') Bluetooth device to read from",
    )
    args = parser.parse_args()

    asyncio.run(read_octahedron(args.device_address))

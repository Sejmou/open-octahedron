import asyncio
from bleak import BleakClient
from pydantic import BaseModel
from typing import Literal
import argparse


class OctahedronPositionChangeEvent(BaseModel):
    """
    The octahedron sends events every time it detects that its position changed.

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


# Timeular's GATT UUIDs (reverse-engineered from BLE sniffing)
ORIENTATION_SERVICE = "c7e70010-c847-11e6-8175-8c89a55d403c"
ORIENTATION_CHAR = "c7e70012-c847-11e6-8175-8c89a55d403c"

"""
The octahedron sends simple numbers to indicate what kind of change was detected.

This dictionary maps the numbers to actual useable events.
"""
NUMBER_TO_EVENT: dict[int, OctahedronPositionChangeEvent] = {
    # adjacent to faces 1-4
    0: OctahedronPositionChangeEvent(change_type="vertex", number=0),
    1: OctahedronPositionChangeEvent(change_type="face", number=1),
    2: OctahedronPositionChangeEvent(change_type="face", number=2),
    3: OctahedronPositionChangeEvent(change_type="face", number=3),
    4: OctahedronPositionChangeEvent(change_type="face", number=4),
    5: OctahedronPositionChangeEvent(change_type="face", number=5),
    6: OctahedronPositionChangeEvent(change_type="face", number=6),
    7: OctahedronPositionChangeEvent(change_type="face", number=7),
    8: OctahedronPositionChangeEvent(change_type="face", number=8),
    9: OctahedronPositionChangeEvent(change_type="vertex", number=9),
    10: OctahedronPositionChangeEvent(change_type="vertex", number=10),
    11: OctahedronPositionChangeEvent(change_type="vertex", number=11),
    12: OctahedronPositionChangeEvent(change_type="vertex", number=12),
    13: OctahedronPositionChangeEvent(change_type="vertex", number=13),
    14: OctahedronPositionChangeEvent(change_type="vertex", number=14),
}


def on_orientation(sender, data: bytearray):
    event_idx = data[0]
    event = NUMBER_TO_EVENT.get(event_idx)
    if event is None:
        # shouldn't really happen afaik, but just in case...
        print(f"Unknown event: {event_idx}")
        return

    print(event)


async def read_tracker(tracker_address: str):
    async with BleakClient(tracker_address) as client:
        print(f"Connected: {client.is_connected}")
        await client.start_notify(ORIENTATION_CHAR, on_orientation)
        print("Listening for orientation changes... (Ctrl+C to stop)")
        await asyncio.sleep(3600)  # listen for 1 hour


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tracker_address",
        type=str,
        help="The address of the octahedron (officially sold as 'Time Tracking Cube') Bluetooth device to read from",
    )
    args = parser.parse_args()

    asyncio.run(read_tracker(args.tracker_address))

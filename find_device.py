import asyncio
from bleak import BleakScanner


async def find_octahedron():
    """
    Searches for the octahedron (officially sold as 'Time Tracking Cube') Bluetooth device, printing its address if found.
    """
    print(
        "Searching for the octahedron (officially sold as 'Time Tracking Cube')...\nNOTE: make sure EARLY (formerly Timeular) is NOT running and already connected"
    )
    devices = await BleakScanner.discover(timeout=5.0)
    tracker = next((d for d in devices if d.name and "Timeular" in d.name), None)
    print()
    if tracker:
        print(
            f"Found: {tracker.name}\nCopy the device's address below and try it out with `read_events.py`:\n{tracker.address}"
        )
    else:
        print("Device not found.")
        print(
            "Just in case the device might have been acutally missed, here's the list of all Bluetooth devices that were found (copy the address if you thing it's the actual device)"
        )
        for d in devices:
            print(f"  {d.address}: {d.name}")


asyncio.run(find_octahedron())

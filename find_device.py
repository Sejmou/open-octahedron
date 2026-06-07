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
    # Timeular is the former name of the device's manufacturer
    # TODO: find out if recent versions of the cube actually use a different device name (can't test as I only own older 'Timeular' trackers)
    octahedron = next((d for d in devices if d.name and "Timeular" in d.name), None)
    print()
    if octahedron:
        print(
            f"Found: {octahedron.name}\nCopy the device's address below and try it out with `read_data.py`:\n{octahedron.address}"
        )
    else:
        print(
            "Device not found automatically. These are all the other detected devices:"
        )
        for d in devices:
            print(f"  {d.address}: {d.name}")

        print(
            "\nPlease check if one of those looks like the tracker to you and try its address with `read_data.py` instead."
            "\n"
            "\nIf you think you found a better way to detect the device reliably, please suggest a fix to help others too:\n"
            "  https://github.com/Sejmou/open-octahedron/issues/new?title=Suggestion%3A+better+way+to+find+the+tracker+device&body=%3C%21--+How+would+you+improve+device+detection%3F+Please+provide+your+suggestion+based+on+things+you+observed+%F0%9F%99%8F+--%3E"
        )


asyncio.run(find_octahedron())

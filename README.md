# Open Octahedron

This very basic Python project demonstrates how to directly read the data from the Bluetooth-enabled octahedron (eight-sided cube) sold by [EARLY](https://early.app/) (formerly called Timeular) as a ['Time Tracking Cube']() for use with their proprietary cloud-based app (forcing you to pay a monthly subscription and hand over your time tracking data to them).

This opens the device up for any use case you can think of, including using it with your own tracking app of choice (assuming you can code or trust your AI to do it for you 😉).

## How it works

The octahedron uses Bluetooth Low Energy (BLE) to communicate with the device that reads data from it. It also emits updates to its orientation through a so-called 'GATT characteristic' that is identified by a UUID. We can connect to its 'notify' property to get notified about every change as it happens.

> NOTE: As it's a fairly basic BLE device, the octahedron does not 'pair' with your computer in the traditional sense like you might be used to from other devices (e.g. headphones)

This repository contains two fairly basic scripts that are meant to be run in sequence, hopefully giving you a good starting point for your own endeavors:

1. `find_device.py`: Searches for the octahedron ('Time Tracking Cube') Bluetooth device, printing its address if found.
2. `read_data.py`: Reads basic information about the octahedron and listens for data about its orientation (using the address found in the previous step and passed as an argument to the script). Also demonstrates how to turn the raw data into easier to interpret 'Change Events', and prints each event to the console as it happens.

## Requirements

- Python 3.12+
- [Bleak](https://github.com/hbldh/bleak) (BLE library for Python)
- [Pydantic](https://github.com/pydantic/pydantic) (not that essential honestly, but used for creating nice 'Change Event' objects from the raw data the Bluetooth device sends)

## Installation

I prefer using uv for running Python code (it's much faster than the basic Python `venv` + `pip install` + `venv` workflow, but probably also quite a bit less intuitive for non-developers).

With `uv` installed, you can install the dependencies with `uv sync`.

```bash
uv sync
```

Then, you can run the scripts with `uv run <script>`.

```bash
uv run read_data.py <device_address>
```

If you prefer the traditional way, you can also just do the following:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, you can run the scripts with `python <script> <device_address>`.

## Related Work

Admittedly, I didn't come up with the logic entirely on my own. I started out with a search prompt + chat convo on Perplexity, which gave me some starter code, and also mentioned the following related projects:

- [hackaru-timeular](https://github.com/pSub/hackaru-timeular): a tool for integrating the Time Tracking Cube with the (now defunct) Hackaru open source time tracking app.
- [timeular-reader](https://github.com/krzysztof-ciszewski/timeular-reader): another tool integrating the Time Tracking Cube with other time tracking apps (Toggl + Clockify) - written in Rust, so it's surely blazingly fast lol

Personally, I plan to implement my own integration with _yet another_ time tracking app, [solidtime](https://github.com/solidtime-io/solidtime), which is fully self-hostable and open source (AGPLv3). Updates may follow soon!

## Helpful Tools

- [LightBlue](https://punchthrough.com/lightblue/): iOS/Android (and Mac!) app for BLE scanning and debugging - also works nicely with the octahedron!

# Open Octahedron

This very basic Python project demonstrates how to directly read the data from the Bluetooth-enabledoctahedron (eight-sided cube) sold by EARLY (formerly called Timeular) as a 'Time Tracking Cube', opening it up for use outside of the proprietary (and, in my humble opinion, overpriced) EARLY app that forces users to pay a monthly subscription fee.

The repo consists of two fairly basic scripts that are meant to be run in sequence, hopefully giving you a good starting point for your own endeavors (in the age of AI you can surely hack something cool together quite quickly lol):

1. `find_device.py`: Searches for the octahedron ('Time Tracking Cube') Bluetooth device, printing its address if found.
2. `read_events.py`: Listens for data sent from the octahedron Bluetooth device (using the address found in the previous step and passed as an argument), turning them into easier to interpret 'Change Events', and printing them to the console.

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
uv run read_events.py <device_address>
```

If you prefer the traditional way, you can also just do the following:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, you can run the scripts with `python <script> <device_address>`.

## Related Work

Admittedly, I didn't come up with the logic entirely on my own. I prompted Perplexity, which gave me some starter code, and also mentioned the following related projects:

- [hackaru-timeular](https://github.com/pSub/hackaru-timeular): a tool for integrating the Time Tracking Cube with the (now defunct) Hackaru open source time tracking app.
- [timeular-reader](https://github.com/krzysztof-ciszewski/timeular-reader): another tool integrating the Time Tracking Cube with other time tracking apps (Toggl + Clockify) - written in Rust, so it's surely blazingly fast lol

Personally, I plan to implement my own integration with _yet another_ time tracking app, [solidtime](https://github.com/solidtime-io/solidtime), which is fully self-hostable and open source (AGPLv3). Updates may follow soon!

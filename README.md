# Drawererer

Prototyping a system to draw things with Python to an image-like array, and spit out the outputs to a web browser for easy visualisation.

## Architecture

`DisplayApp` creates a `Flask` app and sets up a place to draw and store the images being sent to it.
It expects a JPEG image (as bytes) which it displays on the main page, defined by `index.html`.
This uses some web magic that I don't fully understand like `mimetype="multipart/x-mixed-replace; boundary=frame"` but I will understand one day!

`Simulation` is a base class for producing grids, which are each step of the simulation, and converting them to `JPEG` byte sequences in a predicatable manner.
The user is expected to subclass this then: setup all state in the `__init__` method and implement a `step()` generator which `yeild`s arrays for the `emit_jpeg()` method to convert to JPEG bytes.  

## Basic Example

Take a look at `src/demo.py` for an example, the project is managed with `uv` so run:

```bash
uv sync
uv run src/demo.py
```

and navigate to the url logged to the terminal.

## Future Work

- [ ] Can we setup a server to link in multiple simulations, and how would that look? Difference "pages"?
- [ ] When we reload the server in debug mode we get hot reloading (yay!) but we have to refresh the webpage. Can we use sockets to avoid this?
- [ ] It's a bigger scope, but it would be great to get information back from the webpage about mouse clicks/movements - which sockets might let us do?

# Web Drawerer

System to run simulations in Python and split out the outputs to a web browser.

## Architecture

To create a page that show a video we need to provide a function that yields the jpeg payload
The conversion between a grid and jpeg is pretty standard

This can just be a function, see current 'main.py'.
But for reusability it would be great to have this setup somewhere we could just import the "app" and have it run.
And ideally all the boilerplate of converting to a JPEG would be handled too.

So can have a base class `Simulation` which has methods:

- `step`
- `emit_jpeg`

where `step` will be a user defined frame generator, and `emit_jpeg` has a default which just wraps the output in the jpeg conversion.
Users can then subclass this and define their own `__init__` and `step` to make the view work as they want.

On the Flask side, ideally we want the app invokation to be a single line in a `main` function, and as a bonus having the changes detectable by the hot-reloadings debug system would be amazing.

Something like `DisplayApp(address=...,port=...,simulator_intance=...).run()` on the last line
So `DisplayApp()` needs to setup Flask, and create a function decorated with the `app_route` so that it's drawn on the `index.html` page.
For starters, it makes sense to have a simulation per app, which means that actually the `app_route` should always be the same and drawn directly to the index.
But we could maybe customise the title in the html?

## Future Work

Can we setup a server to link in multiple simulations, and how would that look? Difference "pages"?

# Contributing

The goal of this library is to be the go-to library
for calculating everything related to the Black-Scholes-Merton model.
There are always exciting ideas that can still be implemented.
Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues) if you are interested in picking up an existing issue.

## Before you build a feature

- Fork [CarloLepelaars/blackscholes](https://github.com/CarloLepelaars/blackscholes) from Github.

- Install `blackscholes` including development dependencies:

```commandline
pip install uv
uv pip install -e ".[dev]"
```

- Discuss what you want to implement on [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues) before creating a Pull Request.
- Consider and communicate if you would be open to maintain this feature in the future.

## Tests
Please write tests for every new feature that is implemented.
When dealing with complicated formulas, see if you can check your outputs
against an existing software library to guarantee good output.
If you don't know how to do this, the community might be able to help out with performing checks.

Also don't forget to document your new feature. 
Check out this documentation to decide if you should
add a section to an existing doc file or even create a new Markdown file.

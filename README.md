
# ToolDefGenerator

ToolDefGenerator is a Python package designed to automatically generate tool descriptions suitable for the tools argument
in a `client.chat.completions.create` call. It gathers the data by introspection.


## Features

- **Automatic Tool Description**: Generates tool descriptions from Python function definitions
- **Type Mapping**: Maps Python data types to a predefined set of string representations.
- **Function Name Mapping**: Maps function names.
- **Strict Mode**: Enforces strict requirements for docstrings and type annotations.

## Requirements

This package requires `typing.Annotated` to be available, so Python 3.9.0 and higher is required. 

## Installation

You can install ToolDefGenerator by cloning the repository and installing it via pip:

```bash
git clone https://github.com/yourrepository/ToolDefGenerator.git
cd ToolDefGenerator
pip install .
```

When working on the package it is useful to install it in editable form:
```bash
pip install -r requirements.txt
pip install -e .
```

Then test:
```bash
pytest -v tests
```

## Usage

To use ToolDefGenerator, you need to instantiate it and pass it the functions you want to introspect
to the `generate` method.

### Example

```python
from tool_def_generator import ToolDefGenerator
from typing import Annotated


# Define the functions
def example_function(param1: Annotated[str, "The first parameter"],
                     param2: Annotated[str, "The second parameter"]) -> str:
    """
    This is an example function.
    """
    pass


def example_function2(param1: Annotated[str, "The first parameter"],
                      param2: Annotated[str, "The second parameter"]) -> str:
    """
    This is another example function.
    """
    pass


# Create an instance of ToolDefGenerator
generator = ToolDefGenerator()

# Generate tool descriptions using the new generate method
tools = generator.generate(example_function, example_function2)

# Use the generated tools in your client.chat.completions.create call
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

```
For more examples see tests.

## API Reference

### Class `ToolDefGenerator`

A class for generating descriptions of Python functions.

#### `__init__(self, type_map=None, strict=True, name_mappings: List[Tuple[str, str]] = None)`

Initializes the ToolDefGenerator.

- `type_map`: Maps Python types to strings (default provided).
- `strict`: Enforces strict checking for annotations and docstrings.
- `name_mappings`: List of tuples for custom name mappings of functions.

#### `generate(self, *functions: Callable) -> list`

Generates a description array for given functions.

- `*functions`: Functions to introspect.
- Returns: List of tool descriptions for each function.

### Internal Method `introspect(self, function: Callable)`

Introspects a given function (used internally).

- `function`: The function to introspect.
- Returns: Dictionary with the function's name, description, and parameters.


## TODO
 
- use `typing-extensions` package to get access to `typing.Annotated` in older versions of Python

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## License

This project is licensed under the [MIT License](LICENSE).

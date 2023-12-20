
# ToolDefGenerator

ToolDefGenerator is a Python package designed to automatically generate tool descriptions suitable for the tools argument
in a `client.chat.completions.create` call. It gathers the data by introspection.


## Features

- **Automatic Tool Description**: Generates tool descriptions from Python function definitions
- **Type Mapping**: Maps Python data types to a predefined set of string representations.
- **Strict Mode**: Enforces strict requirements for docstrings and type annotations.

## Installation

You can install ToolDefGenerator by cloning the repository and installing it via pip:

```bash
git clone https://github.com/yourrepository/ToolDefGenerator.git
cd ToolDefGenerator
pip install .
```
If working on the package it is useful to install it in editable form:
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

To use ToolDefGenerator, you simply need to import the package and pass the functions you want to introspect to the `gen_tools_desc` function.

### Example

```python
from ToolDefGenerator import gen_tools_desc

def example_function(param1: Annotated[str, "The first parameter"], param2: Annotated[str, "The second parameter"]) -> str:
    """
    This is an example function.
    """
    pass

def example_function2(param1: Annotated[str, "The first parameter"], param2: Annotated[str, "The second parameter"]) -> str:
    """
    This is an example function.
    """
    pass

tools = gen_tools_desc(example_function, example_function2)

response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
```

## API Reference

### `gen_tools_desc(*functions: Callable) -> list`

Generates a tools description array for multiple functions.

#### Arguments

- `*functions`: A variable number of functions to introspect.

#### Returns

- A list representing the tools structure.

### `introspect(function: Callable, strict=True)`

Introspects a function to get its name, description, and parameters.

#### Arguments

- `function`: The function to introspect.
- `strict`: Whether to enforce strict mode.

#### Returns

- A dictionary containing the function's name, description, and parameters.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## License

This project is licensed under the [MIT License](LICENSE).

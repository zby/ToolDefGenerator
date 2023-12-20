from typing import Annotated, Callable, get_type_hints, get_args, get_origin
import inspect

TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}

def gen_tools_desc(*functions: Callable) -> list:
    """
    Generates a tools description array for multiple functions.

    Args:
    *functions: A variable number of functions to introspect.

    Returns:
    A list representing the tools structure for a client.chat.completions.create call.
    """
    tools_array = []

    for function in functions:
        # Use the introspect function to get the description of each function
        function_desc = introspect(function)
        tool_item = {
            "type": "function",
            "function": function_desc
        }
        tools_array.append(tool_item)

    return tools_array

def introspect(function: Callable, strict=True):
    """
    Introspect a function to get its name, description, and parameters.
    Throws exceptions for missing docstrings, annotations, or descriptions if strict is True.
    """
    # Get the name
    name = function.__name__

    # Get the description
    if function.__doc__:
        docstring = function.__doc__.strip()
        description = docstring.split("\n")[0].strip()
    else:
        if strict:
            raise ValueError("Function is missing a docstring")
        else:
            description = ""

    # Get the parameters
    parameters = inspect.signature(function).parameters
    params_dict = {}
    type_hints = get_type_hints(function, include_extras=True)
    if not type_hints and strict:
        raise ValueError("Function parameters are missing type annotations")

    for param_name in parameters:
        if not type_hints:
            params_dict[param_name] = {'type': "string", 'description': ""}
        else:
            param_type_hint = type_hints.get(param_name)
            origin = get_origin(param_type_hint)
            if origin is Annotated:
                args = get_args(param_type_hint)
                param_type, param_desc = args
                param_type = TYPE_MAP.get(param_type, "unknown")
            else:
                if strict:
                    raise ValueError(f"Parameter '{param_name}' is missing an annotation")
                else:
                    param_type = TYPE_MAP.get(param_type_hint, "unknown")
                    param_desc = ""
            params_dict[param_name] = {
                'type': param_type,
                'description': param_desc if param_desc else ""
            }
    for param_name, param_type_hint in type_hints.items():

        args = get_args(param_type_hint)
        if len(args) == 2:
            param_type, param_desc = args
            param_type = TYPE_MAP.get(param_type, "unknown")
            params_dict[param_name] = {
                'type': param_type,
                'description': param_desc if param_desc else ""
            }
        else:
            if strict:
                raise ValueError(f"Parameter '{param_name}' is missing an annotation")
            else:
                params_dict[param_name] = {'type': "string", 'description': ""}

    result = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": params_dict,
            "required": list(params_dict.keys())
        }
    }
    return result

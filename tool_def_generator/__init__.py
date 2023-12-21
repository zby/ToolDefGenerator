from typing import Annotated, Callable, get_type_hints, get_args, get_origin
import inspect
from typing import List, Tuple
from collections import OrderedDict



class ToolDefGenerator:
    def __init__(self, type_map=None, strict=True, name_mappings: List[Tuple[str, str]] = None):
        if type_map is None:
            type_map = {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
            }
        self.type_map = type_map
        self.strict = strict
        self.name_mapping = {original: custom for original, custom in name_mappings} if name_mappings else {}

    def generate(self, *functions: Callable) -> list:
        """
        Generates a tools description array for multiple functions.

        Args:
        *functions: A variable number of functions to introspect.

        Returns:
        A list representing the tools structure for a client.chat.completions.create call.
        """
        tools_array = []
        for function in functions:
            # Check return type
            return_type = get_type_hints(function).get('return')
            if return_type is not None and return_type != str:
                raise ValueError(f"Return type of {function.__name__} is not str")

            function_desc = self.introspect(function)
            tool_item = {
                "type": "function",
                "function": function_desc,
            }
            tools_array.append(tool_item)
        return tools_array

    def introspect(self, function: Callable):
        """
        Introspect a function to get its name, description, and parameters.
        Throws exceptions for missing docstrings, annotations, or descriptions if strict is True.
        """

        # Get the description
        if function.__doc__:
            docstring = function.__doc__.strip()
            description = docstring.split("\n")[0].strip()
        else:
            if self.strict:
                raise ValueError("Function is missing a docstring")
            else:
                description = ""

        params_dict = OrderedDict()
        parameters = inspect.signature(function).parameters
        for name, param in parameters.items():
            if param.annotation is inspect._empty:
                if self.strict:
                    raise ValueError(f"Parameter {name} is missing type annotations")
                else:
                    param_type = "string"
                    param_desc = ""
            else:
                origin = get_origin(param.annotation)
                if origin is Annotated:
                    args = get_args(param.annotation)
                    param_type, param_desc = args
                    param_type = self.type_map.get(param_type, "string")
                else:
                    if self.strict:
                        raise ValueError(f"Parameter '{name}' is missing description annotation")
                    else:
                        param_type = self.type_map.get(param.annotation, "string")
                        param_desc = ""

            params_dict[name] = {
                    'type': param_type,
                    'description': param_desc if param_desc else ""
            }

        # Get the name
        function_name = self.name_mapping.get(function.__name__, function.__name__)
        result = {
            "name": function_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": params_dict,
                "required": list(params_dict.keys())
            }
        }
        return result

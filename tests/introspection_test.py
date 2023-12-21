import pytest
import inspect

from typing import Annotated, get_type_hints, get_args
from tool_def_generator import ToolDefGenerator

# Sample function to be introspected
def sample_function(param1: Annotated[str, "The first parameter"], param2: Annotated[int, "The second integer parameter"]):
    """
    This function does something.
    This is not relevant to the introspection.
    """
    pass

def extra_empty_line(param1: Annotated[str, "The first parameter"]):
    """

    This function does something.
    This is not relevant to the introspection.
    """
    pass

def function3(param3: Annotated[bool, "Description for param3"] = True):
    """Function 3 description."""
    pass

def test_introspect():
    generator = ToolDefGenerator()
    # Call the introspect function on sample_function
    result = generator.introspect(sample_function)

    # Assert for the name
    assert result["name"] == "sample_function"

    # Assert for the description
    assert result["description"] == "This function does something."

    # Assert for the structure of parameters
    assert "parameters" in result
    assert result["parameters"]["type"] == "object"
    assert "properties" in result["parameters"]
    assert "required" in result["parameters"]
    assert result["parameters"]["required"] == ["param1", "param2"]

    # Assert for param1
    assert "param1" in result["parameters"]["properties"]
    assert result["parameters"]["properties"]["param1"]["type"] == "string"
    assert result["parameters"]["properties"]["param1"]["description"] == "The first parameter"

    # Assert for param2
    assert "param2" in result["parameters"]["properties"]
    assert result["parameters"]["properties"]["param2"]["type"] == "integer"
    assert result["parameters"]["properties"]["param2"]["description"] == "The second integer parameter"

    result = generator.introspect(extra_empty_line)

    # Assert for the name
    assert result["name"] == "extra_empty_line"

    # Assert for the description
    assert result["description"] == "This function does something."

# Function without a docstring
def function_no_docstring(param1: Annotated[str, "The first parameter"], param2: Annotated[str, "The second parameter"]):
    pass

# Function with a docstring but no description
def function_missing_description(param1: str, param2: str):
    """
    This function does something.
    """
    pass

# Function with parameters lacking annotations
def function_no_annotations(param1, param2):
    """
    Function description.
    """
    pass

# Function where the second annotation (description) is missing

def test_introspect_failures():
    generator = ToolDefGenerator(strict=True)
    with pytest.raises(ValueError):
        generator.introspect(function_no_docstring)

    with pytest.raises(ValueError):
        generator.introspect(function_missing_description)

    with pytest.raises(ValueError):
        generator.introspect(function_no_annotations)

def test_introspect_nostrict():
    # Should not raise an exception when strict is False
    generator = ToolDefGenerator(strict=False)

    result = generator.introspect(function_no_docstring)
    assert result['description'] == ""

    result = generator.introspect(function_missing_description)
    assert result['parameters']['properties'] == {
        'param1': {'type': 'string', 'description': ''},
        'param2': {'type': 'string', 'description': ''},
    }

    result = generator.introspect(function_no_annotations)
    assert result['parameters']['properties'] == {
        'param1': {'type': 'string', 'description': ''},
        'param2': {'type': 'string', 'description': ''},
    }


class TestClass:
    def __init__(self):
        pass

    def some_method(self, param1: Annotated[str, "The first parameter"],
                    param2: Annotated[str, "The second parameter"]):
        """
        This method does something.
        """
        pass

    def no_args_method(self):
        """
        This method does something.
        """
        pass

def test_introspect_methods():

    test_object = TestClass()
    generator = ToolDefGenerator(ignore_first_param=True)
    result = generator.introspect(test_object.some_method)
    assert result['parameters']['properties']['param1']['description'] == 'The first parameter'
    assert result['parameters']['properties']['param2']['description'] == 'The second parameter'
    result = generator.introspect(test_object.no_args_method)
    assert result['description'] == "This method does something."
    assert result['parameters']['properties'] == {}

import pytest
from tool_def_generator import gen_tools_desc, introspect
from typing import Annotated, get_type_hints, get_args

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
    # Call the introspect function on sample_function
    result = introspect(sample_function)

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

    result = introspect(extra_empty_line)

    # Assert for the name
    assert result["name"] == "extra_empty_line"

    # Assert for the description
    assert result["description"] == "This function does something."


def test_gen_tools_desc():
    tools = gen_tools_desc(sample_function, extra_empty_line, function3)

    # Assert that the tools array has three items
    assert len(tools) == 3

    # Check each tool's structure and content
    for tool in tools:
        assert tool["type"] == "function"
        assert "function" in tool
        function_info = tool["function"]

        # Assert the presence of name, description, and parameters
        assert "name" in function_info
        assert "description" in function_info
        assert "parameters" in function_info

        # Introspect each function manually and compare
        expected_info = introspect(globals()[function_info["name"]])
        assert function_info == expected_info

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
    with pytest.raises(ValueError):
        introspect(function_no_docstring, strict=True)

    with pytest.raises(ValueError):
        introspect(function_missing_description, strict=True)

    with pytest.raises(ValueError):
        introspect(function_no_annotations, strict=True)

def test_introspect_nostrict():
    # Should not raise an exception when strict is False

    result = introspect(function_no_docstring, strict=False)
    assert result['description'] == ""

    result = introspect(function_missing_description, strict=False)
    assert result['parameters']['properties'] == {
        'param1': {'type': 'string', 'description': ''},
        'param2': {'type': 'string', 'description': ''},
    }

    result = introspect(function_no_annotations, strict=False)
    assert result['parameters']['properties'] == {
        'param1': {'type': 'string', 'description': ''},
        'param2': {'type': 'string', 'description': ''},
    }

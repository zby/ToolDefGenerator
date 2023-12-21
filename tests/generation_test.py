import pytest
from tool_def_generator import ToolDefGenerator

def test_initialization():
    # Test default initialization
    generator = ToolDefGenerator()
    assert generator.strict
    assert generator.type_map == {str: "string", int: "integer", float: "number", bool: "boolean"}

    # Test custom initialization
    custom_type_map = {str: "custom_string"}
    custom_name_mappings = [("func", "custom_func")]
    generator = ToolDefGenerator(type_map=custom_type_map, strict=False, name_mappings=custom_name_mappings)
    assert not generator.strict
    assert generator.type_map == custom_type_map
    assert generator.name_mapping == {"func": "custom_func"}


def test_generate_with_name_mapping():
    # Define test functions
    def func1():
        """Function one"""
        return "result1"

    def func2():
        """Function two"""
        return "result2"

    def func3():
        """Function three"""
        return "result3"

    # Create a ToolDescGenerator instance with a name mapping for func2
    name_mappings = [("func2", "custom_func2")]
    generator = ToolDefGenerator(name_mappings=name_mappings)

    # Generate tool descriptions
    tools_desc = generator.generate(func1, func2, func3)

    # Assert the length of the tools array
    assert len(tools_desc) == 3

    # Assert the names are as expected, especially the custom mapped one
    assert tools_desc[0]["name"] == "func1"
    assert tools_desc[1]["name"] == "custom_func2"  # Custom name for func2
    assert tools_desc[2]["name"] == "func3"

    # Additional assertions can be added to check the structure and content of the descriptions

def test_return_type_checking():
    generator = ToolDefGenerator(strict=True)

    def test_func_wrong_return_type() -> int:
        return 1

    with pytest.raises(ValueError):
        generator.generate(test_func_wrong_return_type)


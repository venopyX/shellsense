import pytest
from tools.tool_manager import ToolManager

def test_tool_manager_query():
    manager = ToolManager()
    response = manager.process_query("What is the current stock price of AAPL?")
    assert isinstance(response, str)
    assert "AAPL" in response

def test_tool_manager_invalid_query():
    manager = ToolManager()
    response = manager.process_query("Invalid test query for error handling.")
    assert isinstance(response, str)
    assert "Unable to process" in response

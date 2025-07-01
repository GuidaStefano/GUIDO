import pytest
from unittest.mock import patch, Mock
from src.intent_handling.tools import CultureInspectorTool

tool = CultureInspectorTool()

@patch("src.intent_handling.tools.requests.post")
def test_culture_inspector_empty_list(mock_post):
    """
    Verifica che una lista vuota come input ritorni errore di formattazione.
    """
    mock_post.return_value = Mock(status_code=200, json=Mock(side_effect=Exception("Invalid JSON")))

    data = []
    result = tool.execute_tool(data)
    assert result == ["the list of developers is not well formed", "500"]


@patch("src.intent_handling.tools.requests.post")
def test_culture_inspector_missing_nationality(mock_post):
    """
    Verifica che un dizionario senza chiave 'nationality' venga trattato come input non valido.
    """
    mock_post.return_value = Mock(status_code=200, json=Mock(side_effect=Exception("Invalid JSON")))

    data = {"number": 1000}
    result = tool.execute_tool(data)
    assert result == ["the list of developers is not well formed", "500"]


@patch("src.intent_handling.tools.requests.post")
def test_culture_inspector_success(mock_post):
    """
    Verifica che l'input corretto ritorni le metriche di dispersione culturale.
    """
    expected_response = {
        "idv": 11.018476844566461,
        "ind": 2.0,
        "lto": 5.0,
        "mas": 11.955627250395782,
        "pdi": 13.118079804840942,
        "uai": 10.497231933093088,
        "null_values": {
            "Panama": ["lto", "ind"]
        }
    }

    mock_post.return_value = Mock(status_code=200, json=Mock(return_value=expected_response))

    data = {"number": 1000, "nationality": "Germany"}
    result = tool.execute_tool(data)
    assert result == expected_response

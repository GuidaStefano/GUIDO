import pytest
from unittest.mock import patch, MagicMock
from src.intent_handling.intent_resolver import IntentResolver
from src.intent_handling.cadocs_intent import CadocsIntents


@patch('src.intent_handling.intent_resolver.CsDetectorTool')
def test_get_smells_without_date(mock_tool_cls):
    """
    Verifica che l'intent GetSmells venga risolto usando CsDetectorTool senza formattazione data.
    """
    mock_tool_instance = MagicMock()
    mock_tool_instance.execute_tool.return_value = ["mocked-result"]
    mock_tool_cls.return_value = mock_tool_instance

    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.GetSmells, ["repo-name"])
    assert result == ["mocked-result"]
    mock_tool_instance.execute_tool.assert_called_once()


@patch('src.intent_handling.intent_resolver.CsDetectorTool')
def test_get_smells_with_date_formatting(mock_tool_cls):
    """
    Verifica che l'intent GetSmellsDate converta correttamente la data e usi CsDetectorTool.
    """
    mock_tool_instance = MagicMock()
    mock_tool_instance.execute_tool.return_value = ["mocked-date-result"]
    mock_tool_cls.return_value = mock_tool_instance

    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.GetSmellsDate, ["repo", "01/07/2024"])
    assert result == ["mocked-date-result"]
    args = mock_tool_instance.execute_tool.call_args[0][0]
    assert args[1] == "2024-07-01"


def test_info_intent_returns_empty():
    """
    Verifica che l'intent Info restituisca una lista vuota.
    """
    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.Info, [])
    assert result == []


def test_report_intent_returns_empty():
    """
    Verifica che l'intent Report restituisca una lista vuota.
    """
    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.Report, [])
    assert result == []


@patch('src.intent_handling.intent_resolver.CultureInspectorTool')
def test_geodispersion_intent(mock_tool_cls):
    """
    Verifica che l'intent Geodispersion venga risolto usando CultureInspectorTool.
    """
    mock_tool_instance = MagicMock()
    mock_tool_instance.execute_tool.return_value = {"idv": 10}
    mock_tool_cls.return_value = mock_tool_instance

    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.Geodispersion, [{"number": 1000, "nationality": "Germany"}])
    assert result == {"idv": 10}
    mock_tool_instance.execute_tool.assert_called_once()


@patch('src.intent_handling.intent_resolver.CommunityInspectorTool')
def test_community_inspector_analyze(mock_tool_cls):
    """
    Verifica che l'intent CommunityInspectorAnalyze venga risolto usando CommunityInspectorTool.
    """
    mock_tool_instance = MagicMock()
    mock_tool_instance.execute_tool.return_value = {"status": "SUCCESS"}
    mock_tool_cls.return_value = mock_tool_instance

    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.CommunityInspectorAnalyze, {"author": "foo"})
    assert result["status"] == "SUCCESS"
    mock_tool_instance.execute_tool.assert_called_once()


@patch('src.intent_handling.intent_resolver.CommunityInspectorTool')
def test_community_inspector_results(mock_tool_cls):
    """
    Verifica che l'intent CommunityInspectorResults venga risolto usando CommunityInspectorTool.
    """
    mock_tool_instance = MagicMock()
    mock_tool_instance.execute_tool.return_value = {"job_id": "123", "status": "PENDING"}
    mock_tool_cls.return_value = mock_tool_instance

    resolver = IntentResolver()
    result = resolver.resolve_intent(CadocsIntents.CommunityInspectorResults, {"job_id": "123"})
    assert result["status"] == "PENDING"
    mock_tool_instance.execute_tool.assert_called_once()

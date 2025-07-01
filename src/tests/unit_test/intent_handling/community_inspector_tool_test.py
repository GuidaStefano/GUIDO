import pytest
from unittest.mock import patch, Mock
from requests.exceptions import RequestException
from src.intent_handling.tools import CommunityInspectorTool

tool = CommunityInspectorTool()


@patch('src.intent_handling.tools.requests.post')
def test_analyze_success(mock_post):
    """
    Simula l'avvio di un'analisi TOAD tramite POST /analyze con una risposta di successo.
    Verifica che venga restituito correttamente il job_id.
    """
    mock_post.return_value = Mock(status_code=200, json=lambda: {
        "job_id": "04cf0926-1443-47f9-ba50-e66f80a73ef2"
    })
    data = {"author": "foo", "repository": "bar", "end_date": "2024-01-01"}
    result = tool.execute_tool(data)
    assert result["job_id"] == "04cf0926-1443-47f9-ba50-e66f80a73ef2"


@patch('src.intent_handling.tools.requests.post')
def test_analyze_failure(mock_post):
    """
    Simula un errore (es. timeout o errore server) durante POST /analyze.
    Verifica che venga restituito un errore generico gestito.
    """
    mock_post.side_effect = RequestException("Timeout")
    data = {"author": "foo", "repository": "bar", "end_date": "2024-01-01"}
    result = tool.execute_tool(data)
    assert result == ["Error Starting Community Inspector Analysis", "500"]


@patch('src.intent_handling.tools.requests.get')
def test_status_pending(mock_get):
    """
    Simula il caso in cui GET /status/{job_id} restituisce stato PENDING o STARTED.
    Verifica che lo stato intermedio venga gestito e restituito correttamente.
    """
    mock_get.return_value = Mock(status_code=200, json=lambda: {
        "job_id": "3cae6c4b-2f58-4876-a6c6-23fb4be8bd6b",
        "status": "STARTED",
        "author": "composer",
        "repository": "composer",
        "start_date": "2025-01-31",
        "end_date": "2025-05-01"
    })
    data = {"job_id": "3cae6c4b-2f58-4876-a6c6-23fb4be8bd6b"}
    result = tool.execute_tool(data)
    assert result["status"] == "STARTED"


@patch('src.intent_handling.tools.requests.get')
def test_status_failed(mock_get):
    """
    Simula il caso in cui GET /status/{job_id} restituisce stato FAILED.
    Verifica che venga restituito l'errore completo incluso il messaggio.
    """
    mock_get.return_value = Mock(status_code=200, json=lambda: {
        "job_id": "e687a545-1aec-42c3-ae45-7e26b68afa8d",
        "status": "FAILED",
        "author": "composer",
        "repository": "composer",
        "start_date": "2025-01-31",
        "end_date": "2025-05-01",
        "error": "Invalid Repository: There must be at least 100 commits!"
    })
    data = {"job_id": "e687a545-1aec-42c3-ae45-7e26b68afa8d"}
    result = tool.execute_tool(data)
    assert result["status"] == "FAILED"
    assert "error" in result


@patch('src.intent_handling.tools.requests.get')
def test_status_success_result_ok(mock_get):
    """
    Simula il flusso completo:
    GET /status/{job_id} restituisce SUCCESS → segue GET /result/{job_id}.
    Verifica che il risultato finale contenga 'results', 'patterns' e 'metrics'.
    """
    def side_effect(url, *args, **kwargs):
        if "status" in url:
            return Mock(status_code=200, json=lambda: {"status": "SUCCESS"})
        elif "result" in url:
            return Mock(status_code=200, json=lambda: {
                "author": "bundler",
                "end_date": "2019-06-01",
                "job_id": "56c75a8f-4466-4d0f-80d4-4f54ec7ec864",
                "repository": "bundler",
                "status": "SUCCESS",
                "start_date": "2019-03-03",
                "results": {
                    "graph": {
                        "edges": [{"source": "natesholland", "target": "ryanfox1985", "weight": 2.0}],
                        "nodes": ["natesholland", "ryanfox1985"]
                    },
                    "metrics": {
                        "dispersion": {
                            "geo_distance_variance": {
                                "value": 18462473.22,
                                "description": "Variance in the geographic locations of contributors."
                            }
                        },
                        "structure": {
                            "repo_connections": {
                                "value": True,
                                "description": "Contributors collaborate on same repositories"
                            }
                        }
                    },
                    "patterns": [
                        {"name": "Informal Community (IC)", "detected": True},
                        {"name": "Community of Practice (CoP)", "detected": False}
                    ]
                }
            })

    mock_get.side_effect = side_effect
    data = {"job_id": "56c75a8f-4466-4d0f-80d4-4f54ec7ec864"}
    result = tool.execute_tool(data)
    assert result["status"] == "SUCCESS"
    assert "results" in result
    assert "patterns" in result["results"]
    assert "metrics" in result["results"]


@patch('src.intent_handling.tools.requests.get')
def test_status_success_result_error(mock_get):
    """
    Simula un errore durante GET /result/{job_id} dopo che /status ha restituito SUCCESS.
    Verifica che venga restituito l'errore generico previsto.
    """
    def side_effect(url, *args, **kwargs):
        if "status" in url:
            return Mock(status_code=200, json=lambda: {"status": "SUCCESS"})
        elif "result" in url:
            raise RequestException("Errore nel recupero dei risultati")
    mock_get.side_effect = side_effect
    data = {"job_id": "any-id"}
    result = tool.execute_tool(data)
    assert result == ["Error With Community Inspector Results", "500"]


def test_malformed_input():
    """
    Testa il caso in cui venga fornito un input malformato o incompleto.
    Verifica che venga restituito un errore 500 per parametri non validi.
    """
    data = {"invalid": "value"}
    result = tool.execute_tool(data)
    assert result == ["The Parameters are not well formed!", "500"]


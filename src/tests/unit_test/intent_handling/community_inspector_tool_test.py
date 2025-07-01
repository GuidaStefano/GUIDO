import pytest
from unittest.mock import patch, Mock
from requests.exceptions import RequestException
from src.intent_handling.tools import CommunityInspectorTool

tool = CommunityInspectorTool()

# Simula l'avvio di un'analisi TOAD (POST /analyze)
@patch('src.intent_handling.tools.requests.post')
def test_analyze_success(mock_post):
    mock_post.return_value = Mock(status_code=200, json=lambda: {
        "job_id": "04cf0926-1443-47f9-ba50-e66f80a73ef2"
    })
    data = {"author": "foo", "repository": "bar", "end_date": "2024-01-01"}
    result = tool.execute_tool(data)
    assert result["job_id"] == "04cf0926-1443-47f9-ba50-e66f80a73ef2"

# Simula un fallimento durante POST /analyze (es. timeout)
@patch('src.intent_handling.tools.requests.post')
def test_analyze_failure(mock_post):
    mock_post.side_effect = RequestException("Timeout")
    data = {"author": "foo", "repository": "bar", "end_date": "2024-01-01"}
    result = tool.execute_tool(data)
    assert result == ["Error Starting Community Inspector Analysis", "500"]

# Simula GET /status/{job_id} con stato STARTED
@patch('src.intent_handling.tools.requests.get')
def test_status_pending(mock_get):
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

# Simula GET /status/{job_id} che restituisce FALLIMENTO
@patch('src.intent_handling.tools.requests.get')
def test_status_failed(mock_get):
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

# Simula stato SUCCESS e recupero risultato completo
@patch('src.intent_handling.tools.requests.get')
def test_status_success_result_ok(mock_get):
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

# Simula errore durante il recupero di /result/{job_id} dopo SUCCESS
@patch('src.intent_handling.tools.requests.get')
def test_status_success_result_error(mock_get):
    def side_effect(url, *args, **kwargs):
        if "status" in url:
            return Mock(status_code=200, json=lambda: {"status": "SUCCESS"})
        elif "result" in url:
            raise RequestException("Errore nel recupero dei risultati")
    mock_get.side_effect = side_effect
    data = {"job_id": "any-id"}
    result = tool.execute_tool(data)
    assert result == ["Error With Community Inspector Results", "500"]

# Input privo di chiavi riconosciute → errore formattazione
def test_malformed_input():
    data = {"invalid": "value"}
    result = tool.execute_tool(data)
    assert result == ["The Parameters are not well formed!", "500"]


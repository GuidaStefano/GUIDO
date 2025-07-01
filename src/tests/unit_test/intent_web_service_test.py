import pytest
from unittest.mock import patch, MagicMock
from src.intent_web_service import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('src.intent_web_service.IntentManager')
@patch('src.intent_web_service.resolve_utils')
def test_resolve_message_intent(mock_resolve_utils, mock_intent_manager, client):
    """
    Testa il caso in cui venga passato un messaggio libero e venga predetto un intent via IntentManager.
    """
    mock_intent_manager.return_value.detect_intent.return_value = (
        MagicMock(value='test_intent'),
        {"key": "value"},
        None,
        "en"
    )
    mock_resolve_utils.return_value = ("OK", 200)

    response = client.post('/resolve_intent', json={"message": "Hello world!"})
    assert response.status_code == 200
    mock_resolve_utils.assert_called_once()
    args, _ = mock_resolve_utils.call_args
    assert args[0]["intent"] == "test_intent"
    assert args[0]["entities"] == {"key": "value"}


@patch('src.intent_web_service.resolve_utils')
def test_resolve_job_id(mock_resolve_utils, client):
    """
    Testa il caso in cui venga passato solo un job_id: intent community_inspector_results.
    """
    mock_resolve_utils.return_value = ("OK", 200)
    response = client.post('/resolve_intent', json={"job_id": "abc123"})
    assert response.status_code == 200
    mock_resolve_utils.assert_called_once()
    args, _ = mock_resolve_utils.call_args
    assert args[0]["intent"] == "community_inspector_results"
    assert args[0]["entities"]["job_id"] == "abc123"


@patch('src.intent_web_service.resolve_utils')
def test_resolve_repo_analysis(mock_resolve_utils, client):
    """
    Testa il caso in cui venga passato author, repository, end_date: intent community_inspector_analyze.
    """
    mock_resolve_utils.return_value = ("OK", 200)
    response = client.post('/resolve_intent', json={
        "author": "foo", "repository": "bar", "end_date": "2024-01-01"
    })
    assert response.status_code == 200
    mock_resolve_utils.assert_called_once()
    args, _ = mock_resolve_utils.call_args
    assert args[0]["intent"] == "community_inspector_analyze"
    assert args[0]["entities"]["author"] == "foo"


@patch('src.intent_web_service.resolve_utils')
def test_resolve_geodispersion(mock_resolve_utils, client):
    """
    Testa il caso generico in cui vengano passate direttamente le entità (es. geodispersion).
    """
    mock_resolve_utils.return_value = ("OK", 200)
    response = client.post('/resolve_intent', json={
        "entities": [{"number": 1000, "nationality": "Germany"}]
    })
    assert response.status_code == 200
    mock_resolve_utils.assert_called_once()
    args, _ = mock_resolve_utils.call_args
    assert args[0]["intent"] == "geodispersion"


def test_resolve_invalid_json(client):
    """
    Testa un input malformato (es. nessun JSON) → ritorna 400.
    """
    response = client.post('/resolve_intent', data="non-json", content_type='text/plain')
    assert response.status_code == 400
    assert b"Invalid request: JSON required" in response.data
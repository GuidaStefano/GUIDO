import pytest
from unittest.mock import patch, mock_open
from src.service import cadocs_messages as cm
from src.intent_handling.cadocs_intent import CadocsIntents

mock_smell_data = [{
    "acronym": "CMT",
    "name": "Coordination Breakdown",
    "emoji": "💥",
    "description": "Teams do not coordinate",
    "strategies": [
        {"strategy": "Daily stand-up", "stars": "⭐⭐⭐"},
        {"strategy": "Shared roadmap", "stars": "⭐⭐"}
    ]
}]


@patch("builtins.open", new_callable=mock_open, read_data='[]')
@patch("json.load", return_value=mock_smell_data)
def test_build_cs_message_with_date_en(mock_json, mock_file):
    """
    ✅ Verifica la generazione del messaggio in inglese con data inclusa.
    """
    smells = ["CMT"]
    entities = ["repoX", "2024-07-01"]
    lang = "en"
    text = cm.build_cs_message(smells, entities, lang)
    assert "Hi 👋🏼" in text
    assert "CMT" in text
    assert "Daily stand-up" in text


@patch("builtins.open", new_callable=mock_open, read_data='[]')
@patch("json.load", return_value=mock_smell_data)
def test_build_cs_message_without_date_it(mock_json, mock_file):
    """
    ✅ Verifica la generazione del messaggio in italiano senza data.
    """
    smells = ["CMT"]
    entities = ["repoX"]
    lang = "it"
    text = cm.build_cs_message(smells, entities, lang)
    assert "Ciao 👋🏼" in text
    assert "Strategie" in text or "strategie" in text
    assert "Daily stand-up" in text


def test_build_report_message_en():
    """
    ✅ Verifica la costruzione di un messaggio riepilogativo in inglese.
    """
    text = cm.build_report_message("SMELL DETECTION", ["CMT", "SOC"], ["repo", "2024-01-01"], "en")
    assert "Hi 👋🏼" in text
    assert "*Type:*" in text
    assert "CMT" in text


def test_build_report_message_it():
    """
    ✅ Verifica la costruzione del messaggio riepilogativo in italiano.
    """
    text = cm.build_report_message("DETECTION", ["SCP"], ["repo", "2023-10-10"], "it")
    assert "Ciao 👋🏼" in text
    assert "*Tipo:*" in text
    assert "SCP" in text


@patch("builtins.open", new_callable=mock_open, read_data='[]')
@patch("json.load", return_value=mock_smell_data)
def test_build_info_message_en(mock_json, mock_file):
    """
    ✅ Verifica il messaggio info in inglese con elenco degli smells.
    """
    text = cm.build_info_message("en")
    assert "These are the *community smells*" in text
    assert "Coordination Breakdown" in text


@patch("builtins.open", new_callable=mock_open, read_data='[]')
@patch("json.load", return_value=mock_smell_data)
def test_build_info_message_it(mock_json, mock_file):
    """
    ✅ Verifica il messaggio info in italiano con elenco degli smells.
    """
    text = cm.build_info_message("it")
    assert "Questi sono i *community smells*" in text
    assert "Coordination Breakdown" in text


def test_build_error_message_en():
    """
    ✅ Verifica il messaggio d'errore generico in inglese.
    """
    msg = cm.build_error_message("en")
    assert "I did not understand your intent" in msg


def test_build_error_message_it():
    """
    ✅ Verifica il messaggio d'errore generico in italiano.
    """
    msg = cm.build_error_message("it")
    assert "non sono riuscito a comprendere" in msg


def test_build_custom_error_message():
    """
    ✅ Verifica che venga ritornato direttamente il messaggio custom (posizione 0 dell’array).
    """
    msg = cm.build_custom_error_message(["Errore!", "500"])
    assert msg == "Errore!"


@patch("src.service.cadocs_messages.build_cs_message", return_value="CS-MESSAGE")
def test_build_message_smell_success(mock_cs_msg):
    """
    ✅ Verifica che build_message inoltri correttamente il risultato a build_cs_message.
    """
    result = cm.build_message(["CMT", 200], CadocsIntents.GetSmells, ["repo"], "en")
    assert result == "CS-MESSAGE"


def test_build_message_smell_error():
    """
    ✅ Verifica gestione dell'errore 890 in build_message per community smells.
    """
    result = cm.build_message(["Errore CS", 890], CadocsIntents.GetSmells, ["repo"], "en")
    assert result == "Errore CS"


def test_build_message_report():
    """
    ✅ Verifica che venga usato build_report_message per l’intent Report.
    """
    msg = cm.build_message(["Smell1", "Smell2"], CadocsIntents.Report, ["repo", "2024-01-01", "SMELL DETECTION"], "it")
    assert "Risultati" in msg


@patch("src.service.cadocs_messages.build_info_message", return_value="INFO-MESSAGE")
def test_build_message_info(mock_info):
    """
    ✅ Verifica che venga usato build_info_message per l’intent Info.
    """
    result = cm.build_message("ignored", CadocsIntents.Info, [], "it")
    assert result == "INFO-MESSAGE"


def test_build_message_geodispersion():
    """
    ✅ Verifica che build_message ritorni direttamente i risultati per Geodispersion.
    """
    data = {"idv": 15}
    result = cm.build_message(data, CadocsIntents.Geodispersion, [], "en")
    assert result == data


def test_build_message_fallback():
    """
    ✅ Verifica il messaggio di fallback per intent sconosciuto.
    """
    result = cm.build_message(None, "UNKNOWN_INTENT", [], "en")
    assert "did not understand your intent" in result

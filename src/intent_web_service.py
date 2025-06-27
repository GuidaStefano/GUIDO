import traceback
import uuid
import requests
from flask import Flask, json, jsonify, redirect, request, make_response, url_for

from src.intent_handling.cadocs_intent import CadocsIntents
from src.intent_handling.intent_resolver import IntentResolver
from src.chatbot.intent_manager import IntentManager
from flask_cors import CORS, cross_origin

from src.service.cadocs_messages import build_message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def build_intent(intent_value: str) -> CadocsIntents:
    """
    Funzione che restituisce l'intent legato al valore.
    L'esigenza di tale funzione nasce dal fatto che una enum (CadocsIntents) non è serializzabile
    dunque si deve passare il valore dell'enum alle nostre API.

    Parameters
    -----------
    intent_value: value che viene passato dal client

    Returns
    -----------
    CadocsIntents: intent corrispondente al valore stringa input

    Raises
    -----------
    ValueError: viene sollevata un'eccezione nel momento in cui si passa una stringa che non corrisponde ad alcun intent
    """
    for intent in CadocsIntents:
        if intent_value == intent.value:
            return intent

    raise ValueError(f"Unknown intent: {intent_value}")


def resolve_utils(data: dict, lang: str):
    """
    Funzione che si occupa di risolvere un intent richiamando IntentResolver.
    """
    # se c'è il campo message
    if 'intent' not in data or 'entities' not in data:
        return jsonify({"error": "Invalid request: 'intent' and 'entities' fields required"}), 400

    try:
        resolver = IntentResolver()
        intent = build_intent(data['intent'])
        result = resolver.resolve_intent(intent, data['entities'])
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "An error occurred while resolving intent: " + str(e)}), 500
    return jsonify(build_message(result, build_intent(data['intent']), data['entities'], lang))


@app.route('/resolve_intent', methods=['POST'])
@cross_origin()
def resolve():
    """
    Funzione che si occupa di risolvere un intent richiamando IntentResolver.

    Parameters
    ----------
    data: json
        Può contenere uno dei seguenti formati:

        1. Analisi da testo libero (Chatbot - intent predetto automaticamente con CADOCS NLU):
            {
                "message": "stringa del messaggio"
            }

        2. Richiesta esplicita per tool CommunityInspector - avvio analisi:
            {
                "author": "nomeAutore",
                "repository": "nomeRepository",
                "end_date": "YYYY-MM-DD"
            }

        3. Richiesta esplicita per tool CommunityInspector - recupero risultati:
            {
                "job_id": "uuid-del-task"
            }

        4. Richiesta Esplicita per tool GeoDispersion:
            {
                "entities": [
                    {"number": 1000, "nationality": "Germany"},
                    {"number": 500, "nationality": "Italy"},
                    ...
                ]
            }

    Returns
    -------
    json
        Risultato dell'analisi dell'intent e dell'esecuzione dello strumento associato.
        Se l'input non è valido, restituisce un errore 400.
    """
    try:
        data = request.get_json()
        # se c'è il campo message bisogna predirre l`intent
        if 'message' in data:
            intent_manager = IntentManager()
            intent, entities, _, lang = intent_manager.detect_intent(data["message"])
            data = {"intent": intent.value, "entities": entities}
        # se c`è job_id l`intent è community_inspector_results
        elif 'job_id' in data:
            entities = {
                "job_id": data['job_id']
            }
            data = {"intent": "community_inspector_results", "entities": entities}
            lang = " "
        # se ci sono author, repository ed end_date l`intent è community_inspector_analyze
        elif 'author' in data and 'repository' in data and 'end_date' in data:
            entities = {
                "author": data['author'],
                "repository": data['repository'],
                "end_date": data['end_date']
            }
            data = {"intent": "community_inspector_analyze", "entities": entities}
            lang = " "
        else:
            # se non c'è message è probabilmente un geo-dispersion
            data = {"intent": "geodispersion", "entities": data['entities']}
            lang = " "

    except :
        return jsonify({"error": "Invalid request: JSON required"}), 400

    return resolve_utils(data, lang)
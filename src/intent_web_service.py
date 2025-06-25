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

numReq = 0

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
    -----------
    data: json contenente il messaggio da analizzare che può essere di due tipi:
        {
            "message": "stringa del messaggio"
        }
        oppure
        {
            "entities": [
                {"number": 1000, "nationality": "Germany"},
                {"number": 1000, "nationality": "Italy"}
            ]
        }
    Returns
    -----------
    json: risultato dell'analisi del messaggio
    """
    global numReq
    try:
        data = request.get_json()
        # se c'è il campo message
        if 'message' in data:
            intent_manager = IntentManager()
            intent, entities, _, lang = intent_manager.detect_intent(data["message"])
            data = {"intent": intent.value, "entities": entities}
        # TODO: questo è solo uno stub per provare le richieste dal frontend
        elif 'job_id' in data:
            if numReq < 3:
                numReq += 1
                return jsonify({"job_id": data['job_id'], "status": "PENDING", "author": "daniele_rossi", "repository": "toad-wrapper", "start_date": "2017-01-31", "end_date": "2017-05-01"})
            else:
                return jsonify({
                    "job_id": data['job_id'],
                    "status": "SUCCESS",
                    "results": {
                        "author": "daniele_rossi",
                        "repository": "toad-wrapper",
                        "patterns": [
                            {
                                "name": "Informal Community (IC)",
                                "description": "Usually sets of people part of an organization, with a common interest, often closely dependent on their practice. Informal interactions, usually across unbound distances.",
                                "detected": True
                            },
                            {
                                "name": "Community of Practice (CoP)",
                                "description": "Groups of people sharing a concern, a set of problems, or a passion about a topic, who deepen their knowledge and expertise in this area by interacting frequently in the same geolocation.",
                                "detected": False
                            },
                            {
                                "name": "Formal Network (FN)",
                                "description": "Members are rigorously selected and prescribed by management (often in the form of FG), directed according to corporate strategy and mission.",
                                "detected": True
                            },
                            {
                                "name": "Social Network (SN)",
                                "description": "SNs can be seen as a supertype for all OSSs. To identify an SN, it is sufficient to split the structure of organizational patterns into macrostructure and microstructure.",
                                "detected": True
                            },
                            {
                                "name": "Informal Network (IN)",
                                "description": "Looser networks of ties between individuals that happen to come in contact in the same context. Their driving force is the strength of the ties between members.",
                                "detected": False
                            },
                            {
                                "name": "Network of Practice (NoP)",
                                "description": "A networked system of communication and collaboration connecting CoPs. Anyone can join. They span geographical and time distances alike.",
                                "detected": True
                            },
                            {
                                "name": "Formal Group (FG)",
                                "description": "People grouped by corporations to act on (or by means of) them. Each group has an organizational goal, called mission. Compared to FN, no reliance on networking technologies, local in nature.",
                                "detected": False
                            },
                            {
                                "name": "Project Team (PT)",
                                "description": "People with complementary skills who work together to achieve a common purpose for which they are accountable. Enforced by their organization and follow specific strategies or organizational guidelines.",
                                "detected": True
                            }
                        ],
                        "metrics": {
                            "dispersion": {
                                "geo_distance_variance": 11354570.939798128,
                                "avg_geo_distance": 3433.8892193812785,
                                "cultural_distance_variance": 22.621716233057025
                            },
                            "engagement": {
                                "m_comment_per_pr": 0.0,
                                "mm_comment_dist": 1.0,
                                "m_watchers": 0,
                                "m_stargazers": 0.0,
                                "m_active": 1.0,
                                "mm_commit_dist": 0.0,
                                "mm_filecollab_dist": 2.0
                            },
                            "formality": {
                                "m_membership_type": 1.9166666666666667,
                                "milestones": 36,
                                "lifetime": 6274
                            },
                            "longevity": 77.8,
                            "structure": {
                                "repo_connections": True,
                                "follow_connections": True,
                                "pr_connections": True
                            }
                        },
                        "graph": {
                            "nodes": [
                                "david-durrleman",
                                "anders9ustafsson",
                                "cesarsouza",
                                "alice-martin",
                                "bob-smith",
                                "carla-ruiz",
                                "deepak-sharma",
                                "elena-fischer",
                                "fabio-garcia",
                                "gina-lee",
                                "haruto-yamada",
                                "ivan-petrov"
                            ],
                            "edges": [
                                {"source": "david-durrleman", "target": "anders9ustafsson", "weight": 1},
                                {"source": "david-durrleman", "target": "alice-martin", "weight": 2},
                                {"source": "anders9ustafsson", "target": "cesarsouza", "weight": 3},
                                {"source": "alice-martin", "target": "bob-smith", "weight": 1},
                                {"source": "carla-ruiz", "target": "david-durrleman", "weight": 2},
                                {"source": "deepak-sharma", "target": "carla-ruiz", "weight": 2},
                                {"source": "elena-fischer", "target": "alice-martin", "weight": 1},
                                {"source": "fabio-garcia", "target": "gina-lee", "weight": 1},
                                {"source": "gina-lee", "target": "haruto-yamada", "weight": 3},
                                {"source": "haruto-yamada", "target": "ivan-petrov", "weight": 2},
                                {"source": "bob-smith", "target": "fabio-garcia", "weight": 1},
                                {"source": "deepak-sharma", "target": "elena-fischer", "weight": 1},
                                {"source": "ivan-petrov", "target": "carla-ruiz", "weight": 2}
                            ]
                        }
                    }
                })
        # TODO: questo è solo uno stub per provare le richieste dal frontend
        elif 'author' in data and 'repository' in data and 'end_date' in data:
            job_id = str(uuid.uuid4())
            numReq = 0
            return jsonify({"job_id": job_id}), 200
        else:
            # se non c'è message è probabilmente un geo-dispersion
            data = {"intent": "geodispersion", "entities": data['entities']}
            lang = " "

    except :
        return jsonify({"error": "Invalid request: JSON required"}), 400

    print("STO PROCESSANDO RISPOSTA...")

    return resolve_utils(data, lang)
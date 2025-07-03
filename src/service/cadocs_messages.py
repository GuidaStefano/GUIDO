import json
from src.intent_handling.cadocs_intent import CadocsIntents
from src.service.language_handler import LanguageHandler
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
path_to_smells = os.path.join(parent_dir,'community_smells.json')

#Sistemare la classe
def build_cs_message(smells, entities, lang): # entities qui è un dict proveniente da IntentManager
    # Testo che verrà restituito
    text = ""
    repo_name = entities.get("repo", "repository name not found") # Usa .get() per sicurezza
    date_str = entities.get("date") # Potrebbe essere None se l'intent è GetSmells senza data

    if lang == "en":
        text += f"Hi 👋🏼\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"

    if date_str: # Se c'è una data nelle entità (tipico di GetSmellsDate)
        if lang == "en":
            text += f"These are the community smells we were able to detect in the repository {repo_name} starting from {date_str}:\n"
        elif lang == "it":
            text += f"Questi sono i community smells che siamo stati in grado di rilevare nella repository {repo_name} a partire da {date_str}:\n"
    else: # Se non c'è una data (tipico di GetSmells)
        if lang == "en":
            text += f"These are the community smells we were able to detect in the repository {repo_name}:\n"
        elif lang == "it":
            text += f"Questi sono i community smells che siamo stati in grado di rilevare nella repository {repo_name}:\n"



    if lang == "en":
        # Aggiunta del testo per ogni smell rilevato
        with open(path_to_smells, encoding='utf-8') as fp:
            data = json.load(fp)
            for s in smells: # 's' qui è l'acronimo dello smell (o ciò che si presume sia)
                smell_data_list = [sm_json for sm_json in data if sm_json["acronym"] == s]
                text += f"----------------------------\n"
                if smell_data_list:
                    smell_details = smell_data_list[0]
                    text += f"*{s}* {smell_details.get('name')} {smell_details.get('emoji')}\n_{smell_details.get('description')}_\n"
                    strategies = smell_details.get("strategies")
                    if strategies and len(strategies) > 0:
                        text += "Some possible mitigation strategies are:\n"
                        for st in strategies:
                            text += f">{st.get('strategy')}\n{st.get('stars')}\n"
                else:
                    text += f"*{s}* - Details not found for this item.\n" # Messaggio di fallback
    elif lang == "it":
        # path_to_smells_it = os.path.join(parent_dir,'community_smells_it.json') # Assumendo esista un file per IT
        # with open(path_to_smells_it, encoding='utf-8') as fp: # O usa lo stesso file e traduci i campi
        with open(path_to_smells, encoding='utf-8') as fp: # Usando lo stesso file JSON per ora
            data = json.load(fp)
            for s in smells:
                smell_data_list = [sm_json for sm_json in data if sm_json["acronym"] == s]
                text += f"----------------------------\n"
                if smell_data_list:
                    smell_details = smell_data_list[0]
                    # Qui idealmente si tradurrebbero name, description, strategy dalle smell_details
                    text += f"*{s}* {smell_details.get('name')} {smell_details.get('emoji')}\n_{smell_details.get('description')}_\n"
                    strategies = smell_details.get("strategies")
                    if strategies and len(strategies) > 0:
                        text += "Alcune possibili strategie per la mitigazione sono:\n"
                        for st in strategies:
                            text += f">{st.get('strategy')}\n{st.get('stars')}\n"
                else:
                    text += f"*{s}* - Dettagli non trovati per questo elemento.\n" # Messaggio di fallback

    if lang == "en":
        text += "----------------------------\nSee you soon 👋🏼"
    elif lang == "it":
        text += "----------------------------\nA presto 👋🏼"

    return text

def build_report_message(exec_type, results, entities, lang):
    #lang = LanguageHandler().get_current_language()
    
    # Testo che verrà restituito
    text = ""

    if lang == "en":
        text += f"Hi 👋🏼\n"
        text += "This is a summary of your last execution\n"
        text += f"*Type:*\n{exec_type}\n"
        text += f"*Repository:*\n{entities[0]}\n"
        text += f"*Date:*\n{entities[1]}\n"
        text += "*Results:*\n" + "\n".join(results) + "\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"
        text += "Questo è una sintesi della tua ultima esecuzione\n"
        text += f"*Tipo:*\n{exec_type}\n"
        text += f"*Repository:*\n{entities[0]}\n"
        text += f"*Data:*\n{entities[1]}\n"
        text += "*Risultati:*\n" + "\n".join(results) + "\n"

    return text

def build_info_message(lang):
    #lang = LanguageHandler().get_current_language()

    # Testo che verrà restituito
    text = ""

    if lang == "en":
        text += f"Hi 👋🏼\n"
        text += "These are the *community smells* I can detect in your development communities:\n"
    elif lang == "it":
        text += f"Ciao 👋🏼\n"
        text += "Questi sono i *community smells* che riesco a individuare nelle vostre community:\n"

    # Aggiunta del testo per ogni smell
    if lang == "en":
        with open(path_to_smells, encoding='utf-8') as fp:
            data = json.load(fp)
            for i in data:
                text += f"----------------------------\n*{i.get('name')}*  -  {i.get('acronym')}  -  {i.get('emoji')}\n{i.get('description')}\n"

        if lang == "en":
            text += "----------------------------\nIf you want to remain up-to-date, please follow us on our social networks:\n"
            text += "- Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab>\n"
            text += "- Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab>\n"
            text += "- Website: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io>\n"
            text += "Also, feel free to get in touch with us to have a discussion about the subject by sending us an email at slambiase@unisa.it!"
        
    elif lang == "it":
        with open(path_to_smells, encoding='utf-8') as fp:
            data = json.load(fp)
            for i in data:
                text += f"----------------------------\n*{i.get('name')}*  -  {i.get('acronym')}  -  {i.get('emoji')}\n{i.get('description')}\n"

            text += "----------------------------\nSe volete rimanere aggiornati, seguite i canali social:\n"
            text += "- Instagram: <https://www.instagram.com/sesa_lab/|sesa_lab>\n"
            text += "- Twitter: <https://twitter.com/sesa_lab|@SeSa_Lab>\n"
            text += "- Sito web: <https://sesalabunisa.github.io/en/index.html|sesalabunisa.github.io>\n"
            text += "Inoltre, sentitevi liberi di mettervi in contatto con noi per discutere dell'argomento inviandoci una mail a slambiase@unisa.it!"


    return text

def build_error_message(lang):
    #lang = LanguageHandler().get_current_language()

    # Testo che verrà restituito
    if lang == "en":
        text = f"Hi, I'm sorry but I did not understand your intent. Please be more specific!"
    elif lang == "it":
        text = f"Ciao, mi dispiace ma non sono riuscito a comprendere il suo intent. La prego di essere più specifico!"

    return text


def build_custom_error_message(array):
    result_message = array[0]
    return result_message


# this function will format the message basing on the intent
def build_message(results, intent, entities, lang):
    lh = LanguageHandler() # Ottieni l'istanza singleton

    # Verifica esplicita e sicura dell'attributo translations e imposta la lingua
    translations_dict = getattr(lh, 'translations', {}) # Default a {} se l'attributo non esiste
    if not isinstance(translations_dict, dict):
        translations_dict = {} # Assicura che sia un dizionario se l'attributo esiste ma non è un dict

    if lang and lang.strip(): # Assicura che lang sia una stringa valida
        lang_code = lang.strip()
        if lang_code in translations_dict: # Usa la variabile sicura translations_dict
            lh.current_lang = lang_code
        # else: current_lang rimane il default di LanguageHandler o l'ultimo impostato
    # Se lang è None o vuota, current_lang rimane il default o l'ultimo impostato

    if intent == CadocsIntents.GetSmells or intent == CadocsIntents.GetSmellsDate:
        # Gestione degli errori specifici di CsDetector
        # results atteso in caso di errore: [messaggio_errore, codice_errore]
        if len(results) == 2 and isinstance(results[1], int):
            error_code = results[1]
            error_message_text = results[0]
            repo_name = entities[0] if entities and len(entities) > 0 else "N/A"

            if error_code == 890:
                # Per l'errore 890, build_custom_error_message restituisce solo il testo dell'errore.
                # Lo usiamo ma lo wrappiamo in un dizionario standard.
                # message_text = build_custom_error_message(results) # results[0]
                # Invece di chiamare build_custom_error_message, usiamo direttamente results[0]
                # e lo traduciamo o formattiamo se necessario.
                # Assumiamo che results[0] sia già un messaggio user-friendly per l'errore 890.
                # Se la traduzione è necessaria, lh.translate("cadocs_errors", error_code, ...)
                return {"message": error_message_text, "results": [], "code": error_code}
            elif error_code == 201: # Altro errore gestito da CsDetector
                # Simile a sopra, results[0] è il messaggio di errore.
                # Potrebbe essere necessario tradurre/formattare diversamente.
                # message_text = lh.translate("cadocs_errors", error_code, {"repo_name": repo_name, "error_message": error_message_text})
                return {"message": error_message_text, "results": [], "code": error_code}
            # Altri codici di errore specifici potrebbero essere gestiti qui

        # Caso di successo (o errore non gestito come [str, int_code] sopra)
        # results è una lista di file (stringhe)
        message_text = build_cs_message(results, entities, lang)
        return {"message": message_text, "results": results, "code": 200}

    elif intent == CadocsIntents.Report:
        # build_report_message restituisce una stringa
        message_text = build_report_message(exec_type=entities[2], results=results, entities=entities, lang=lang)
        return {"message": message_text, "results": results, "code": 200}

    elif intent == CadocsIntents.Info:
        # build_info_message restituisce una stringa
        message_text = build_info_message(lang)
        return {"message": message_text, "results": [], "code": 200}

    elif intent == CadocsIntents.Geodispersion:
        # results è già il dizionario corretto da restituire come parte di "results"
        # Aggiungiamo un messaggio generico di successo se non c'è altro.
        # message_text = lh.translate("geodispersion_success_default", "Analysis complete.")
        # Se results è { "pdi": ..., "idv": ... }, allora la risposta sarà:
        # {"message": "...", "results": { "pdi": ..., "idv": ...}, "code": 200 }
        return {"message": "Geodispersion analysis completed.", "results": results, "code": 200}

    elif intent == CadocsIntents.CommunityInspectorAnalyze:
        # results è {"job_id": "..."}
        # message_text = lh.translate("ci_analyze_success_default", f"Analysis started with Job ID: {results.get('job_id')}")
        return {"message": f"Community Inspector analysis started. Job ID: {results.get('job_id')}", "results": results, "code": 200}

    elif intent == CadocsIntents.CommunityInspectorResults:
        # results è {"job_id": ..., "status": ..., "results": ...} (se successo) o {"job_id": ..., "status": ...} (se pending/failed)
        # message_text = lh.translate("ci_results_status_default", f"Job {results.get('job_id')} status: {results.get('status')}")
        return {"message": f"Community Inspector results for Job ID: {results.get('job_id')}. Status: {results.get('status')}", "results": results, "code": 200}

    else: # Intent non gestito o errore generico
        message_text = build_error_message(lang) # build_error_message restituisce una stringa
        return {"message": message_text, "results": [], "code": 400} # Codice di errore client generico
from typing import List
from src.intent_handling.tool_strategy import Tool
import os
import requests
from dotenv import load_dotenv

load_dotenv('src/.env')


# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):
    last_repo = ""

    def execute_tool(self, data: List): # data può essere List o Dict
        print("\n\n\nSono in CsDetectorTool execute_tool, data:", data)

        repo_name = None
        date_param = None

        if isinstance(data, list):
            if len(data) > 0:
                repo_name = data[0]
            if len(data) > 1:
                date_param = data[1] # Formato atteso YYYY-MM-DD
        elif isinstance(data, dict): # Gestisce il caso in cui data è un dict
            repo_name = data.get("repo")
            date_param = data.get("date") # Formato atteso YYYY-MM-DD o DD/MM/YYYY che IntentResolver dovrebbe aver normalizzato
                                          # Tuttavia, IntentResolver non normalizza per GetSmells semplice.
                                          # Se la data arriva qui come DD/MM/YYYY, CsDetector si aspetta YYYY-MM-DD.
                                          # Per ora, assumiamo che se date_param è presente, sia già YYYY-MM-DD.

        if not repo_name:
            return ["Repository name not provided or in incorrect format.", "CSD_ERROR_REPO_MISSING", 890] # Codice errore per build_message

        base_url = os.environ.get('CSDETECTOR_URL_GETSMELLS')
        pat = os.environ.get('PAT', "")

        if date_param:
            # Assicurarsi che date_param sia nel formato YYYY-MM-DD
            # Questa logica di conversione data è duplicata da IntentResolver,
            # idealmente dovrebbe essere centralizzata o CsDetectorTool dovrebbe essere più tollerante.
            # Per ora, se arriva una data, ci fidiamo del formato.
            req_url = f"{base_url}?repo={repo_name}&pat={pat}&start={date_param}"
        else:
            req_url = f"{base_url}?repo={repo_name}&pat={pat}"

        print(f"CsDetectorTool requesting URL: {req_url}\n\n\n")
        req = requests.get(req_url)

        response_json = req.json()

        if req.status_code == 890:
            error_text = response_json.get('error')
            code = response_json.get('code')
            results = [error_text, code]
            print("\n\nRESULTATO\n\n", results)
            return results

        print("\n\n\nStampa risposta", req.json())
        print("\n\n\n")
        # we retrieve the file names created by csdetector
        results = req.json().get("result")[1:]
        return results





class CultureInspectorTool(Tool):
    """
    CultureInspectorTools implements one of the concrete strategies
    within the strategy design pattern.
    This specific strategy enables users to utilize
    the geodispersion inspector for computing
    the cultural geodispersion metrics of their team.
    """
    def execute_tool(self, data: List):
        """
        Executes the CultureInspector tool by calling its webservice.
        :param data: List of dictionaries where each dictionary is built like this:
                {"number": 1000, "nationality": "Germany"}
        :return: A json with the hofstede metrics computed by the CultureInspector tool.
                e.g. {
                    "idv": 11.018476844566461,
                    "ind": 2.0,
                    "lto": 5.0,
                    "mas": 11.955627250395782,
                    "pdi": 13.118079804840942,
                    "uai": 10.497231933093088,
                    "null_values": {
                        "Panama": [
                            "lto",
                            "ind"
                        ]
                    }
                }
                or if the data is not formatted correctly:
                ["the list of developers is not well formed", code = "500"]
        """

        req = requests.post(os.environ.get('GEODISPERSION_URL'), json=data)
        try:
            result = req.json()
        except Exception as e:
            return ["the list of developers is not well formed", "500"]

        return result

#TODO: Sostituire gli URL Hard Coded con ENV
class CommunityInspectorTool(Tool):
    """
        CommunityInspectorTool is a concrete strategy class (Strategy Design Pattern)
        that integrates the TOAD tool into the GUIDO platform.

        It supports two distinct intents:
        - 'community_inspector_analyze': Launches a new TOAD analysis.
        - 'community_inspector_results': Fetches the status or the result of a previous analysis.

        Behavior:
        ---------
        - If the input `data` contains: author, repository, and end_date,
          a POST request is sent to `/analyze` to start the analysis.

            Input Example:
            {
                "author": "bundler",
                "repository": "bundler",
                "end_date": "2019-06-01"
            }

            Output Example (analysis started):
            {
                "job_id": "745225d1-298b-4925-b045-a90bb3a71eae"
            }

        - If the input `data` contains: job_id,
          a GET request is first sent to `/status/{job_id}` to check the job status.

            - If status is not 'SUCCESS', return the current status as-is:
                {
                    "job_id": "...",
                    "status": "PENDING" | "STARTED" | "FAILED",
                    ...
                }

            - If status is 'SUCCESS', a second GET request is sent to `/result/{job_id}`
              to fetch the full analysis result.

                Successful Result Example:
                {
                    "job_id": "...",
                    "status": "SUCCESS",
                    "results": {
                        "patterns": [...],
                        "metrics": {...},
                        "graph": {...}
                    }
                }

                Failed Result Example:
                {
                    "job_id": "...",
                    "status": "FAILED",
                    "error": "Invalid Repository: The Repo should contain at least 100 commits!"
                }
        """

    def execute_tool(self, data: List):

        # === Caso 1: Avviare nuova analisi ===
        if "author" in data and "repository" in data and "end_date" in data:
            try:
                response = requests.post(f"{os.environ.get('TOAD_URL')}/analyze", json=data)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                return ["Error Starting Community Inspector Analysis", "500"]

        # === Caso 2: Recuperare stato o risultato ===
        elif "job_id" in data:
            job_id = data["job_id"]
            try:
                # Recupera lo stato del job
                status_response = requests.get(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
                status_response.raise_for_status()
                status_data = status_response.json()

                # Se il job non è ancora completato, restituisce lo stato
                if status_data.get("status") != "SUCCESS":
                    return status_data

                # Altrimenti recupera il risultato completo
                result_response = requests.get(f"{os.environ.get('TOAD_URL')}/result/{job_id}")
                result_response.raise_for_status()
                return result_response.json()

            except requests.RequestException as e:
                return ["Error With Community Inspector Results", "500"]

        # === Caso non supportato ===
        return ["The Parameters are not well formed!", "500"]

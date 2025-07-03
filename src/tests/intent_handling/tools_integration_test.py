import unittest
from unittest.mock import patch, MagicMock
import os
import requests # Importa il modulo requests
from src.intent_handling.tools import CsDetectorTool, CultureInspectorTool, CommunityInspectorTool

class TestToolsIntegration(unittest.TestCase):

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_csdetector_tool_success(self, mock_get):
        # Mock della risposta di requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": ["header", "file1.txt", "file2.csv"]}
        mock_get.return_value = mock_response

        tool = CsDetectorTool()
        data = ["test_repo"]
        result = tool.execute_tool(data)

        # Verifica che requests.get sia stato chiamato con l'URL corretto
        expected_url = f"{os.environ.get('CSDETECTOR_URL_GETSMELLS')}?repo=test_repo&pat={os.environ.get('PAT', '')}"
        mock_get.assert_called_once_with(expected_url)
        self.assertEqual(result, ["file1.txt", "file2.csv"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_csdetector_tool_with_date_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": ["header", "file_date.txt"]}
        mock_get.return_value = mock_response

        tool = CsDetectorTool()
        data = ["test_repo_date", "2023-01-15"] # La data è già nel formato corretto per il mock
        result = tool.execute_tool(data)

        expected_url = f"{os.environ.get('CSDETECTOR_URL_GETSMELLS')}?repo=test_repo_date&pat={os.environ.get('PAT', '')}&start=2023-01-15"
        mock_get.assert_called_once_with(expected_url)
        self.assertEqual(result, ["file_date.txt"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_csdetector_tool_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 890 # Codice di errore specifico di CsDetector
        mock_response.json.return_value = {"error": "API Error Occurred", "code": "CSD_API_ERROR"}
        mock_get.return_value = mock_response

        tool = CsDetectorTool()
        data = ["error_repo"]
        result = tool.execute_tool(data)
        self.assertEqual(result, ["API Error Occurred", "CSD_API_ERROR"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post')
    def test_culture_inspector_tool_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_metrics = {
            "idv": 10.0, "ind": 5.0, "lto": 7.0,
            "mas": 8.0, "pdi": 6.0, "uai": 9.0,
            "null_values": {}
        }
        mock_response.json.return_value = expected_metrics
        mock_post.return_value = mock_response

        tool = CultureInspectorTool()
        data = [{"number": 10, "nationality": "Italy"}, {"number": 5, "nationality": "Germany"}]
        result = tool.execute_tool(data)

        mock_post.assert_called_once_with(os.environ.get('GEODISPERSION_URL'), json=data)
        self.assertEqual(result, expected_metrics)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post')
    def test_culture_inspector_tool_bad_data(self, mock_post):
        # Simula una risposta di errore dal servizio se i dati non sono ben formati
        # Questo potrebbe essere un errore 400 o 500 a seconda dell'implementazione del servizio reale
        mock_response = MagicMock()
        mock_response.status_code = 400 # o 500
        # Il servizio CultureInspectorTool attualmente gestisce l'eccezione e restituisce un formato specifico
        # mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Error decoding JSON", "doc", 0)
        mock_post.return_value = mock_response
        # Forziamo un errore di decodifica JSON per simulare dati malformati che causano l'eccezione
        mock_response.json.side_effect = Exception("Simulated JSON decode error")


        tool = CultureInspectorTool()
        data = "not_a_list_of_dicts" # Dati chiaramente malformati
        result = tool.execute_tool(data)

        mock_post.assert_called_once_with(os.environ.get('GEODISPERSION_URL'), json=data)
        self.assertEqual(result, ["the list of developers is not well formed", "500"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post')
    def test_community_inspector_tool_analyze_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_job_id = {"job_id": "test-job-123"}
        mock_response.json.return_value = expected_job_id
        mock_post.return_value = mock_response

        tool = CommunityInspectorTool()
        data = {"author": "test_author", "repository": "test_repo", "end_date": "2023-10-01"}
        result = tool.execute_tool(data)

        mock_post.assert_called_once_with(f"{os.environ.get('TOAD_URL')}/analyze", json=data)
        self.assertEqual(result, expected_job_id)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post')
    def test_community_inspector_tool_analyze_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500 # Simula un errore del server
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error")
        mock_post.return_value = mock_response

        tool = CommunityInspectorTool()
        data = {"author": "err_author", "repository": "err_repo", "end_date": "2023-10-01"}
        result = tool.execute_tool(data)

        mock_post.assert_called_once_with(f"{os.environ.get('TOAD_URL')}/analyze", json=data)
        self.assertEqual(result, ["Error Starting Community Inspector Analysis", "500"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_community_inspector_tool_results_pending(self, mock_get):
        job_id = "pending-job-456"

        # Mock per la chiamata a /status/{job_id}
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        pending_status = {"job_id": job_id, "status": "PENDING"}
        mock_status_response.json.return_value = pending_status
        mock_get.return_value = mock_status_response # La prima chiamata a get restituisce lo stato

        tool = CommunityInspectorTool()
        data = {"job_id": job_id}
        result = tool.execute_tool(data)

        mock_get.assert_called_once_with(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
        self.assertEqual(result, pending_status)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_community_inspector_tool_results_success(self, mock_get):
        job_id = "success-job-789"

        # Mock per la chiamata a /status/{job_id}
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        success_status = {"job_id": job_id, "status": "SUCCESS"}
        mock_status_response.json.return_value = success_status

        # Mock per la chiamata a /result/{job_id}
        mock_result_response = MagicMock()
        mock_result_response.status_code = 200
        expected_results = {
            "job_id": job_id,
            "status": "SUCCESS",
            "results": {"patterns": [], "metrics": {}, "graph": {}}
        }
        mock_result_response.json.return_value = expected_results

        # Configura mock_get per restituire risposte diverse in base alla chiamata
        mock_get.side_effect = [mock_status_response, mock_result_response]

        tool = CommunityInspectorTool()
        data = {"job_id": job_id}
        result = tool.execute_tool(data)

        # Verifica le chiamate a mock_get
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
        mock_get.assert_any_call(f"{os.environ.get('TOAD_URL')}/result/{job_id}")

        self.assertEqual(result, expected_results)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_community_inspector_tool_results_status_error(self, mock_get):
        job_id = "error-status-job"

        mock_status_response = MagicMock()
        mock_status_response.status_code = 500 # Errore nel recuperare lo stato
        mock_status_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Status API Error")
        mock_get.return_value = mock_status_response

        tool = CommunityInspectorTool()
        data = {"job_id": job_id}
        result = tool.execute_tool(data)

        mock_get.assert_called_once_with(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
        self.assertEqual(result, ["Error With Community Inspector Results", "500"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_community_inspector_tool_results_result_error(self, mock_get):
        job_id = "error-result-job"

        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {"job_id": job_id, "status": "SUCCESS"}

        mock_result_response = MagicMock()
        mock_result_response.status_code = 500 # Errore nel recuperare i risultati
        mock_result_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Result API Error")

        mock_get.side_effect = [mock_status_response, mock_result_response]

        tool = CommunityInspectorTool()
        data = {"job_id": job_id}
        result = tool.execute_tool(data)

        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
        mock_get.assert_any_call(f"{os.environ.get('TOAD_URL')}/result/{job_id}")
        self.assertEqual(result, ["Error With Community Inspector Results", "500"])

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    def test_community_inspector_tool_bad_parameters(self):
        tool = CommunityInspectorTool()
        data = {"invalid_param": "some_value"} # Parametri non validi
        result = tool.execute_tool(data)
        self.assertEqual(result, ["The Parameters are not well formed!", "500"])


if __name__ == '__main__':
    # Non è più necessario caricare dotenv qui esplicitamente per i test,
    # dato che usiamo @patch.dict per mockare os.environ per ogni test.
    # `tools.py` continuerà a usare `load_dotenv('src/.env')` per l'esecuzione normale,
    # ma durante i test, i valori mockati da @patch.dict avranno la precedenza
    # all'interno del contesto del test specifico.
    unittest.main()

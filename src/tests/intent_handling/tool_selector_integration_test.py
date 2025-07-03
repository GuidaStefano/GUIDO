import unittest
from unittest.mock import MagicMock, patch
import os # Necessario per patch.dict(os.environ, ...)
import requests # Necessario per requests.exceptions.HTTPError
from src.intent_handling.tool_selector import ToolSelector
from src.intent_handling.tools import CsDetectorTool, CultureInspectorTool, CommunityInspectorTool

class TestToolSelectorIntegrationRealTools(unittest.TestCase):

    # Mock delle variabili d'ambiente necessarie per i tool
    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get')
    def test_tool_selector_with_real_csdetector_tool(self, mock_requests_get):
        """
        Testa ToolSelector con un'istanza reale di CsDetectorTool,
        mockando solo la chiamata requests.get sottostante.
        """
        # Configura il mock per requests.get
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        expected_smell_files = ["file1.txt", "file2.csv"]
        mock_response_get.json.return_value = {"result": ["header"] + expected_smell_files}
        mock_requests_get.return_value = mock_response_get

        # Istanza reale del tool
        cs_detector_tool_real = CsDetectorTool()
        selector = ToolSelector(strategy=cs_detector_tool_real)

        input_data = ["my_repo"] # Senza data per semplicità
        actual_result = selector.run(input_data)

        # Verifica che requests.get sia stato chiamato dal tool
        expected_url = f"{os.environ.get('CSDETECTOR_URL_GETSMELLS')}?repo=my_repo&pat={os.environ.get('PAT', '')}"
        mock_requests_get.assert_called_once_with(expected_url)
        # Verifica che il risultato sia quello processato dal tool
        self.assertEqual(actual_result, expected_smell_files)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post')
    def test_tool_selector_with_real_culture_inspector_tool(self, mock_requests_post):
        """
        Testa ToolSelector con CultureInspectorTool reale, mockando requests.post.
        """
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        expected_metrics = {"pdi": 10, "idv": 20}
        mock_response_post.json.return_value = expected_metrics
        mock_requests_post.return_value = mock_response_post

        culture_inspector_tool_real = CultureInspectorTool()
        selector = ToolSelector(strategy=culture_inspector_tool_real)

        input_data = [{"nationality": "Italian", "number": 10}]
        actual_result = selector.run(input_data)

        mock_requests_post.assert_called_once_with(os.environ.get('GEODISPERSION_URL'), json=input_data)
        self.assertEqual(actual_result, expected_metrics)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.post') # Per CommunityInspectorTool - analyze
    def test_tool_selector_with_real_community_inspector_tool_analyze(self, mock_requests_post_analyze):
        """
        Testa ToolSelector con CommunityInspectorTool reale (analyze), mockando requests.post.
        """
        mock_response_analyze = MagicMock()
        mock_response_analyze.status_code = 200
        expected_job_id = {"job_id": "job-123-analyze"}
        mock_response_analyze.json.return_value = expected_job_id
        mock_requests_post_analyze.return_value = mock_response_analyze

        community_inspector_tool_real = CommunityInspectorTool()
        selector = ToolSelector(strategy=community_inspector_tool_real)

        input_data = {"author": "test", "repository": "repo", "end_date": "2023-10-10"}
        actual_result = selector.run(input_data)

        mock_requests_post_analyze.assert_called_once_with(f"{os.environ.get('TOAD_URL')}/analyze", json=input_data)
        self.assertEqual(actual_result, expected_job_id)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get') # Per CommunityInspectorTool - results (status e result)
    def test_tool_selector_with_real_community_inspector_tool_results_success(self, mock_requests_get_results):
        """
        Testa ToolSelector con CommunityInspectorTool reale (results successo), mockando requests.get.
        """
        job_id = "job-456-results"
        # Mock per la chiamata a /status/{job_id}
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {"job_id": job_id, "status": "SUCCESS"}

        # Mock per la chiamata a /result/{job_id}
        mock_result_response = MagicMock()
        mock_result_response.status_code = 200
        expected_full_results = {"job_id": job_id, "status": "SUCCESS", "results": {"data": "some_data"}}
        mock_result_response.json.return_value = expected_full_results

        mock_requests_get_results.side_effect = [mock_status_response, mock_result_response]

        community_inspector_tool_real = CommunityInspectorTool()
        selector = ToolSelector(strategy=community_inspector_tool_real)

        input_data = {"job_id": job_id}
        actual_result = selector.run(input_data)

        self.assertEqual(mock_requests_get_results.call_count, 2)
        mock_requests_get_results.assert_any_call(f"{os.environ.get('TOAD_URL')}/status/{job_id}")
        mock_requests_get_results.assert_any_call(f"{os.environ.get('TOAD_URL')}/result/{job_id}")
        self.assertEqual(actual_result, expected_full_results)

    @patch.dict(os.environ, {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    })
    @patch('requests.get') # Per CsDetectorTool
    @patch('requests.post') # Per CultureInspectorTool
    def test_tool_selector_change_strategy_real_tools(self, mock_post_ci, mock_get_csd):
        """
        Testa che ToolSelector possa cambiare la strategia con tool reali.
        """
        # --- Configurazione per CsDetectorTool ---
        cs_expected_result = ["cs_result.txt"]
        mock_response_csd = MagicMock()
        mock_response_csd.status_code = 200
        mock_response_csd.json.return_value = {"result": ["header"] + cs_expected_result}
        mock_get_csd.return_value = mock_response_csd

        cs_detector_real = CsDetectorTool()
        selector = ToolSelector(strategy=cs_detector_real)
        cs_input_data = ["repo1"]
        self.assertEqual(selector.run(cs_input_data), cs_expected_result)
        expected_csd_url = f"{os.environ.get('CSDETECTOR_URL_GETSMELLS')}?repo=repo1&pat={os.environ.get('PAT', '')}"
        mock_get_csd.assert_called_once_with(expected_csd_url)

        # --- Configurazione per CultureInspectorTool ---
        ci_expected_result = {"pdi": 50}
        mock_response_ci = MagicMock()
        mock_response_ci.status_code = 200
        mock_response_ci.json.return_value = ci_expected_result
        mock_post_ci.return_value = mock_response_ci

        culture_inspector_real = CultureInspectorTool()
        # Cambia strategia
        selector.strategy = culture_inspector_real

        ci_input_data = [{"nationality": "German", "number": 5}]
        self.assertEqual(selector.run(ci_input_data), ci_expected_result)
        mock_post_ci.assert_called_once_with(os.environ.get('GEODISPERSION_URL'), json=ci_input_data)

        # Assicuriamoci che il mock per CSD non sia stato chiamato di nuovo
        mock_get_csd.assert_called_once()


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import os # Per patch.dict(os.environ, ...)
import requests # Per requests.exceptions
from src.intent_handling.intent_resolver import IntentResolver
from src.intent_handling.cadocs_intent import CadocsIntents
# Non importiamo più ToolSelector o i tool specifici qui,
# IntentResolver li userà internamente.

class TestIntentResolverIntegrationRealToolSelector(unittest.TestCase):

    DEFAULT_ENV_VARS = {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token"
    }

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get') # Mock per CsDetectorTool
    def test_resolve_intent_get_smells_real_selector(self, mock_requests_get):
        """
        Testa IntentResolver con ToolSelector reale per GetSmells.
        Mocka solo la chiamata requests.get fatta da CsDetectorTool.
        """
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        expected_smells_files = ["smell1.txt", "smell2.json"]
        mock_response_get.json.return_value = {"result": ["header"] + expected_smells_files}
        mock_requests_get.return_value = mock_response_get

        resolver = IntentResolver()
        intent = CadocsIntents.GetSmells
        entities = ["test/repo"]

        result = resolver.resolve_intent(intent, entities)

        # Verifica che requests.get sia stato chiamato (da CsDetectorTool)
        expected_url = f"{self.DEFAULT_ENV_VARS['CSDETECTOR_URL_GETSMELLS']}?repo=test/repo&pat={self.DEFAULT_ENV_VARS['PAT']}"
        mock_requests_get.assert_called_once_with(expected_url)
        # Verifica che il risultato sia quello processato da CsDetectorTool
        self.assertEqual(result, expected_smells_files)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get') # Mock per CsDetectorTool
    def test_resolve_intent_get_smells_date_real_selector(self, mock_requests_get):
        """
        Testa IntentResolver con ToolSelector reale per GetSmellsDate.
        Verifica la formattazione della data e la chiamata a CsDetectorTool.
        """
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        expected_smells_files = ["smell_dated.txt"]
        mock_response_get.json.return_value = {"result": ["header"] + expected_smells_files}
        mock_requests_get.return_value = mock_response_get

        resolver = IntentResolver()
        intent = CadocsIntents.GetSmellsDate
        entities = ["test/repo/date", "15/01/2023"] # Formato DD/MM/YYYY

        result = resolver.resolve_intent(intent, entities)

        # Verifica che requests.get sia stato chiamato con la data formattata
        # IntentResolver converte "15/01/2023" in "2023-01-15"
        expected_url = f"{self.DEFAULT_ENV_VARS['CSDETECTOR_URL_GETSMELLS']}?repo=test/repo/date&pat={self.DEFAULT_ENV_VARS['PAT']}&start=2023-01-15"
        mock_requests_get.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_smells_files)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post') # Mock per CultureInspectorTool
    def test_resolve_intent_geodispersion_real_selector(self, mock_requests_post):
        """
        Testa IntentResolver con ToolSelector reale per Geodispersion.
        """
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        expected_geo_metrics = {"pdi": 7.8, "idv": 4.5}
        mock_response_post.json.return_value = expected_geo_metrics
        mock_requests_post.return_value = mock_response_post

        resolver = IntentResolver()
        intent = CadocsIntents.Geodispersion
        entities = [{"number": 10, "nationality": "Italian"}, {"number": 5, "nationality": "German"}]

        result = resolver.resolve_intent(intent, entities)

        mock_requests_post.assert_called_once_with(self.DEFAULT_ENV_VARS['GEODISPERSION_URL'], json=entities)
        self.assertEqual(result, expected_geo_metrics)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post') # Mock per CommunityInspectorTool (analyze)
    def test_resolve_intent_community_inspector_analyze_real_selector(self, mock_requests_post):
        """
        Testa IntentResolver con ToolSelector reale per CommunityInspectorAnalyze.
        """
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        expected_analyze_job = {"job_id": "ci-analyze-job-real"}
        mock_response_post.json.return_value = expected_analyze_job
        mock_requests_post.return_value = mock_response_post

        resolver = IntentResolver()
        intent = CadocsIntents.CommunityInspectorAnalyze
        entities = {"author": "auth_real", "repository": "repo_real", "end_date": "2023-12-01"}

        result = resolver.resolve_intent(intent, entities)

        mock_requests_post.assert_called_once_with(f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/analyze", json=entities)
        self.assertEqual(result, expected_analyze_job)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get') # Mock per CommunityInspectorTool (results)
    def test_resolve_intent_community_inspector_results_real_selector(self, mock_requests_get):
        """
        Testa IntentResolver con ToolSelector reale per CommunityInspectorResults.
        """
        job_id = "ci-results-job-real"
        # Mock per chiamata a /status
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {"job_id": job_id, "status": "SUCCESS"}

        # Mock per chiamata a /result
        mock_result_response = MagicMock()
        mock_result_response.status_code = 200
        expected_ci_results = {"job_id": job_id, "status": "SUCCESS", "results": {"detail": "some_real_data"}}
        mock_result_response.json.return_value = expected_ci_results

        mock_requests_get.side_effect = [mock_status_response, mock_result_response]

        resolver = IntentResolver()
        intent = CadocsIntents.CommunityInspectorResults
        entities = {"job_id": job_id}

        result = resolver.resolve_intent(intent, entities)

        self.assertEqual(mock_requests_get.call_count, 2)
        mock_requests_get.assert_any_call(f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/status/{job_id}")
        mock_requests_get.assert_any_call(f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/result/{job_id}")
        self.assertEqual(result, expected_ci_results)

    # I test per Info e Report non usano ToolSelector né tool esterni, quindi rimangono invariati.
    def test_resolve_intent_info(self):
        resolver = IntentResolver()
        intent = CadocsIntents.Info
        entities = []
        result = resolver.resolve_intent(intent, entities)
        self.assertEqual(result, [])

    def test_resolve_intent_report(self):
        resolver = IntentResolver()
        intent = CadocsIntents.Report
        entities = ["some_repo"] # Questo potrebbe essere un bug se Report si aspetta più entità
        result = resolver.resolve_intent(intent, entities)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()

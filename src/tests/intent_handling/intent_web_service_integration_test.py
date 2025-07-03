import sys
from unittest.mock import MagicMock, patch
import unittest
import json
import os
import requests # Per requests.exceptions

# Mock solo per IntentManager per evitare dipendenze NLU/torch.
sys.modules['src.chatbot.intent_manager'] = MagicMock()

from src.intent_web_service import app as flask_app
from src.intent_handling.cadocs_intent import CadocsIntents
from src.service.cadocs_messages import build_message

flask_app.config['TESTING'] = True

class TestIntentWebServiceIntegrationRealResolver(unittest.TestCase):

    DEFAULT_ENV_VARS = {
        "CSDETECTOR_URL_GETSMELLS": "http://csdetector-fake-url.com/api",
        "GEODISPERSION_URL": "http://geodispersion-fake-url.com/api",
        "TOAD_URL": "http://toad-fake-url.com/api",
        "PAT": "test_pat_token" # Aggiunto PAT per CsDetectorTool
    }

    def setUp(self):
        self.client = flask_app.test_client()

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get') # Per mockare la chiamata di CsDetectorTool
    @patch('src.intent_web_service.IntentManager')
    def test_resolve_intent_with_message_get_smells(self, MockIntentManager, mock_requests_get):
        """
        Testa /resolve_intent con 'message' -> GetSmells.
        IntentResolver è reale. CsDetectorTool è reale (modificato per accettare dict). requests.get è mockato.
        IntentManager è mockato.
        """
        mock_intent_manager_instance = MockIntentManager.return_value
        detected_entities_dict = {"repo": "test/repo-message"} # IntentManager restituisce un dict
        mock_intent_manager_instance.detect_intent.return_value = (
            CadocsIntents.GetSmells,
            detected_entities_dict,
            "show me smells in test/repo-message",
            "en"
        )

        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        # CsDetectorTool ora dovrebbe restituire acronimi/identificatori di smell, non nomi di file.
        # Ma per ora, la sua logica interna restituisce ancora nomi di file.
        # E build_cs_message è stato adattato per gestire acronimi non trovati.
        cs_detector_results_list = ["SMELL_X", "SMELL_Y"]
        mock_response_get.json.return_value = {"result": ["header"] + cs_detector_results_list}
        mock_requests_get.return_value = mock_response_get

        request_data = {"message": "show me smells in test/repo-message"}
        response = self.client.post('/resolve_intent', json=request_data)

        self.assertEqual(response.status_code, 200)
        mock_intent_manager_instance.detect_intent.assert_called_once_with(request_data["message"])

        # Verifica che CsDetectorTool (tramite IntentResolver) abbia chiamato requests.get
        repo_name = detected_entities_dict["repo"]
        expected_cs_url = f"{self.DEFAULT_ENV_VARS['CSDETECTOR_URL_GETSMELLS']}?repo={repo_name}&pat={self.DEFAULT_ENV_VARS['PAT']}"
        mock_requests_get.assert_called_once_with(expected_cs_url)

        expected_response_data = build_message(
            cs_detector_results_list,
            CadocsIntents.GetSmells,
            detected_entities_dict,
            "en"
        )
        self.assertEqual(response.json, expected_response_data)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager', MagicMock()) # Non usato in questo flusso diretto
    def test_resolve_intent_community_inspector_analyze_direct(self, mock_requests_post):
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        ci_tool_result = {"job_id": "ci-analyze-real-direct"}
        mock_response_post.json.return_value = ci_tool_result
        mock_requests_post.return_value = mock_response_post

        request_data = {
            "author": "direct_author_ci",
            "repository": "direct_repo_ci",
            "end_date": "2023-12-25"
        }
        response = self.client.post('/resolve_intent', json=request_data)
        self.assertEqual(response.status_code, 200)

        mock_requests_post.assert_called_once_with(
            f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/analyze", json=request_data
        )

        expected_response_data = build_message(
            ci_tool_result,
            CadocsIntents.CommunityInspectorAnalyze,
            request_data,
            " "
        )
        self.assertEqual(response.json, expected_response_data)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get')
    @patch('src.intent_web_service.IntentManager', MagicMock())
    def test_resolve_intent_community_inspector_results_direct(self, mock_requests_get):
        job_id = "ci-results-real-direct"
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = {"job_id": job_id, "status": "SUCCESS"}

        mock_result_response = MagicMock()
        mock_result_response.status_code = 200
        ci_tool_full_results = {"job_id": job_id, "status": "SUCCESS", "results": {"info": "some_ci_data"}}
        mock_result_response.json.return_value = ci_tool_full_results

        mock_requests_get.side_effect = [mock_status_response, mock_result_response]

        request_data = {"job_id": job_id}
        response = self.client.post('/resolve_intent', json=request_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_requests_get.call_count, 2)
        mock_requests_get.assert_any_call(f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/status/{job_id}")
        mock_requests_get.assert_any_call(f"{self.DEFAULT_ENV_VARS['TOAD_URL']}/result/{job_id}")

        # entities per build_message sono quelle costruite da intent_web_service per questo caso
        entities_for_build_message = {"job_id": job_id}
        expected_response_data = build_message(
            ci_tool_full_results,
            CadocsIntents.CommunityInspectorResults,
            entities_for_build_message,
            " "
        )
        self.assertEqual(response.json, expected_response_data)

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager', MagicMock())
    def test_resolve_intent_geodispersion_direct(self, mock_requests_post):
        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        geo_tool_result = {"pdi": 8.0, "idv": 2.1, "lto": 6.3}
        mock_response_post.json.return_value = geo_tool_result
        mock_requests_post.return_value = mock_response_post

        request_data_entities_list = [
            {"number": 200, "nationality": "USA"},
            {"number": 30, "nationality": "Canada"}
        ]
        # L'endpoint per Geodispersion si aspetta un body JSON che sia direttamente la lista,
        # ma internamente lo wrappa in {"entities": lista} per il parsing iniziale,
        # e poi estrae la lista per IntentResolver.
        request_body_for_endpoint = {"entities": request_data_entities_list}

        response = self.client.post('/resolve_intent', json=request_body_for_endpoint)
        self.assertEqual(response.status_code, 200)

        mock_requests_post.assert_called_once_with(
            self.DEFAULT_ENV_VARS['GEODISPERSION_URL'], json=request_data_entities_list
        )

        expected_response_data = build_message(
            geo_tool_result,
            CadocsIntents.Geodispersion,
            request_data_entities_list,
            " "
        )
        self.assertEqual(response.json, expected_response_data)

    def test_resolve_intent_invalid_json(self):
        response = self.client.post('/resolve_intent', data="not json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Invalid request: JSON required")

    @patch.dict(os.environ, DEFAULT_ENV_VARS)
    @patch('requests.get')
    @patch('requests.post')
    @patch('src.intent_web_service.IntentManager')
    def test_resolve_intent_resolver_internal_error(self, MockIntentManager, mock_requests_post, mock_requests_get):
        mock_intent_manager_instance = MockIntentManager.return_value
        mock_intent_manager_instance.detect_intent.return_value = (
            CadocsIntents.GetSmells,
            {"repo": "error/repo"},
            "trigger resolver error",
            "en"
        )

        mock_requests_get.side_effect = requests.exceptions.RequestException("Simulated network error from tool")

        request_data = {"message": "trigger resolver error"}
        response = self.client.post('/resolve_intent', json=request_data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)
        self.assertTrue("An error occurred while resolving intent" in response.json["error"])

        mock_intent_manager_instance.detect_intent.assert_called_once_with(request_data["message"])
        mock_requests_get.assert_called_once()


    def test_build_intent_valid(self):
        intent_val = "get_smells"
        expected_intent = CadocsIntents.GetSmells
        from src.intent_web_service import build_intent
        self.assertEqual(build_intent(intent_val), expected_intent)

    def test_build_intent_invalid(self):
        intent_val = "unknown_intent"
        from src.intent_web_service import build_intent
        with self.assertRaises(ValueError) as context:
            build_intent(intent_val)
        self.assertTrue(f"Unknown intent: {intent_val}" in str(context.exception))

if __name__ == '__main__':
    unittest.main()

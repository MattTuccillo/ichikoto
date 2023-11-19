from django.test import TestCase
from unittest.mock import patch
from ..services.gpt_service import send_prompt


class SendPromptTests(TestCase):

    # successful manual mode response
    def test_send_prompt_success_manual_mode(self):
        response = send_prompt(manual_mode=True)
        expected_response = "Sample response for testing."
        self.assertEqual(response['choices'][0]
                         ['message']['content'], expected_response)

    # handles APIError in manual mode
    def test_send_prompt_api_error_manual_mode(self):
        with self.assertRaises(ValueError) as context:
            send_prompt(manual_mode=True, simulate_error='APIError')
        self.assertIn(
            "OpenAI API returned an API Error: simulated error", str(context.exception))

    # handles APIConnectionError in manual mode
    def test_send_prompt_api_connection_error_manual_mode(self):
        with self.assertRaises(ValueError) as context:
            send_prompt(manual_mode=True, simulate_error='APIConnectionError')
        self.assertIn(
            "Failed to connect to OpenAI API: simulated error", str(context.exception))

    # handles RateLimitError in manual mode
    def test_send_prompt_rate_limit_error_manual_mode(self):
        with self.assertRaises(ValueError) as context:
            send_prompt(manual_mode=True, simulate_error='RateLimitError')
        self.assertIn("OpenAI API request exceeded rate limit: simulated error", str(
            context.exception))

    # test the actual API call (without hitting the API)
    @patch('word_manager.services.gpt_service.client.chat.completions.create')
    def test_send_prompt_api_call(self, mock_api_call):
        mock_api_call.return_value = {"choices": [
            {"message": {"content": "API response"}}]}

        response = send_prompt()
        expected_response = "API response"
        self.assertEqual(response['choices'][0]
                         ['message']['content'], expected_response)
        mock_api_call.assert_called_once()

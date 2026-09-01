import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from chatbot.models import ChatbotSettings
from core.models import PersonalProfile


class ChatbotAndStaticTests(TestCase):
    def setUp(self):
        PersonalProfile.objects.create(
            full_name="Nagasrinivas Govvala",
            title="Software Developer",
            email="test@example.com",
        )
        ChatbotSettings.objects.create(
            is_enabled=True,
            rate_limit_per_hour=20,
        )
        self.client = Client(enforce_csrf_checks=True)

    def test_favicon_route(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 301)
        self.assertIn('/static/favicon.svg', response.url)

    def test_home_renders_csrf_and_favicon(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('meta name="csrf-token"', content)
        self.assertIn('window.CSRF_TOKEN =', content)
        self.assertTrue('favicon' in content and '.svg' in content)

    @patch('urllib.request.urlopen')
    def test_chatbot_post_with_csrf(self, mock_urlopen):
        # Mock OpenRouter response
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            'choices': [{'message': {'content': 'Hello! I am Srinivas AI.'}}]
        }).encode('utf-8')
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        # First make a GET request to obtain the CSRF cookie
        get_resp = self.client.get('/')
        csrf_cookie = get_resp.cookies.get('csrftoken')
        self.assertIsNotNone(csrf_cookie)

        # POST with valid CSRF header returns mocked response
        post_resp = self.client.post(
            '/chatbot/ask/',
            data=json.dumps({'message': 'Hello'}),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_cookie.value,
        )
        self.assertEqual(post_resp.status_code, 200)
        data = post_resp.json()
        self.assertEqual(data.get('response'), 'Hello! I am Srinivas AI.')



from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

class  AccountApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test2025',
            password='test2025@12345',
            email='test2025@gmail.com'
        )

    def test_login(self):
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # 登陆失败，http status code 返回 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',

        })
        # 登陆失败，http status code 返回 400 = BAD_REQUEST
        self.assertEqual(response.status_code, 400)

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test2025@12345',
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'test2025@gmail.com')

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)



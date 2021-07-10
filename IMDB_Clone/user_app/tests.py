from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django.contrib.auth.models import User

class RegisterTestCase(APITestCase):
    def test_register(self):
        data={
            "username":"tesing",
            "password":"testing@gmail.com",
            "password2":"testing@gmail.com",
            "email":"testing@gmail.com"
        }
        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test1',password='password')

    def test_login(self):
        data={
            "username":"test1",
            "password":"password"
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="test1")
        self.client.credentials(HTTP_AUTHORIZATION = "Token "+ self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
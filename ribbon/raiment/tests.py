from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from raiment.models import Message
from .views import SignUp


class Authentication(TestCase):

    def setUp(self):
        print("Starting Authentication Test")
        self.client = APIClient()
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def signUp(self, username, password):
        request = self.factory.post('/signup/',
                                    {
                                        "user": {
                                            "username": username,
                                            "password": password
                                        }
                                    }, format='json')

        response = SignUp.as_view()(request)
        self.assertEqual(response.data["user"]["user"]["username"], username)
        self.password = password
        self.username = username

    def login(self):
        self.client.login(username=self.username, password=self.password)
        token = Token.objects.get(user__username=self.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_details(self):
        self.signUp('TestUser', 'ComplexPass')
        self.login()
        response = self.client.get('/hello/')
        self.assertEqual(response.status_code, 200)


class Messaging(TestCase):
    def setUp(self):
        print("Starting Messaging Test")
        self.client = APIClient()
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def signUp(self, username, password):
        request = self.factory.post('/signup/',
                                    {
                                        "user": {
                                            "username": username,
                                            "password": password
                                        }
                                    }, format='json')

        response = SignUp.as_view()(request)
        self.assertEqual(response.data["user"]["user"]["username"], username)
        self.password = password
        self.username = username

    def login(self):
        self.client.login(username=self.username, password=self.password)
        token = Token.objects.get(user__username=self.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_details(self):
        self.signUp('TestUser', 'ComplexPass')
        self.login()
        self.receiver = User.objects.create(username="TestUserReceiver", password="VeryComplexPass")
        response = self.client.post('/message/',
                                    {"receiver": 'TestUserReceiver',
                                     "txt": "Message sent from " + self.username +
                                            "to TestUserReceiver " + self.receiver.username})

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/message/',
                                    {"receiver": 'TestUserReceiver',
                                     "txt": "Message sent from " + self.username +
                                            "to TestUserReceiver " + self.receiver.username})

        self.assertEqual(response.status_code, 200)

        for i in Message.objects.filter(author__username=self.username):
            var = "Message sent from " + self.username + "to TestUserReceiver " + self.receiver.username
            self.assertEqual(i.txt, var)


class Blocking(TestCase):
    def setUp(self):
        print("Starting Blocking Test")
        self.client = APIClient()
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def signUp(self, username, password):
        #This function is different for there needs to be two clients for this test
        request = self.factory.post('/signup/',
                                    {
                                        "user": {
                                            "username": username,
                                            "password": password
                                        }
                                    }, format='json')

        response = SignUp.as_view()(request)
        self.assertEqual(response.data["user"]["user"]["username"], username)
        self.password = password
        self.username = username
        return User.objects.get(username=username)

    def login(self, username, password, client):
        client.login(username=username, password=password)
        token = Token.objects.get(user__username=username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_details(self):
        self.signUp('TestUser', 'ComplexPass')
        self.client = self.login('TestUser', 'ComplexPass',self.client)
        self.receiver = self.signUp(username="TestUserReceiver", password="VeryComplexPass")
        self.receiverClient = APIClient()
        self.login(username="TestUserReceiver", password="VeryComplexPass", client=self.receiverClient)
        response = self.receiverClient.post('/block/',
                                            {"receiver": self.username})

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/message/',
                                    {"receiver": 'TestUserReceiver',
                                     "txt": "Message sent from " + self.username +
                                            "to TestUserReceiver " + self.receiver.username})

        self.assertEqual(response.status_code, 200)
        self.assertEqual((Message.objects.filter(author__username=self.username).exists()), False)


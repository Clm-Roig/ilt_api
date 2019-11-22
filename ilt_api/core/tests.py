import json
from django.test import Client, TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from core.models import MementoCategory


# ===== TOOL FUNCTIONS
def create_user(user_id, username, email, password):
    """
    Create an user an return the user Object created. There is no check for the id.
    """
    return User.objects.create_user(
        id=user_id, username=username, email=email, password=password,
    )


def get_auth_token(username: str, password: str):
    """
    Return an authentication token without any exception handling
    """
    response = Client().post(
        "/v1/auth/token/", {"username": username, "password": password}
    )
    return json.loads(response.content)["access"]


# ===================


class AuthWithTokenTests(TestCase):
    def setUp(self):
        self.client = Client()
        create_user(1, "user1", "user1@user1.com", "top_secret")
        create_user(2, "user2", "user2@user2.com", "top_secret")

    def test_token_auth_ok_200(self):
        response = self.client.post(
            "/v1/auth/token/", {"username": "user1", "password": "top_secret"}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_auth_fail_401(self):
        response = self.client.post(
            "/v1/auth/token/", {"username": "randomuser", "password": "randompwd"}
        )
        self.assertEqual(response.status_code, 401)


class MementoCategoriesTests(APITestCase):
    def setUp(self):
        self.user1 = create_user(1, "user1", "user1@user1.com", "top_secret")
        self.user2 = create_user(2, "user2", "user2@user2.com", "top_secret")
        self.auth_token_1 = get_auth_token("user1", "top_secret")
        # pylint: disable=no-member
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token_1)
        # pylint: enable=no-member

        self.m_cat1 = MementoCategory.objects.create(id=1, name="Cat1", user_id=1)
        self.m_cat2 = MementoCategory.objects.create(id=2, name="Cat2", user_id=2)

    def test_get_all(self):
        url = "/v1/memento_categories/"
        response = self.client.get(url, format="json")
        content = json.loads(response.content)
        self.assertEqual(content["count"], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_one_200(self):
        url = "/v1/memento_categories/1/"
        response = self.client.get(url, format="json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"], 1)
        self.assertEqual(content["name"], "Cat1")

    def test_get_one_404(self):
        url = "/v1/memento_categories/123456789/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 404)

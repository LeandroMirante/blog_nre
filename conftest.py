import pytest
from app.users.models import User
from app.articles.models import Category
from django.shortcuts import reverse
import json
import ast
import base64

# User 1
@pytest.fixture
def user1(db):
    return User.objects.create_user(
        name="Username 1",
        email="leandro.mirante@hotmail.com",
        phone=12345,
        password="geladeira55",
    )


@pytest.fixture
def token_user1(db, client, user1):
    response = client.post(
        reverse("login"),
        data=json.dumps(
            {"email": "leandro.mirante@hotmail.com", "password": "geladeira55"}
        ),
        content_type="application/json",
    )

    return ast.literal_eval(response.json().get("tokens"))["access"]


# User 2
@pytest.fixture
def user2(db):
    return User.objects.create_user(
        name="Username 2",
        email="user2@hotmail.com",
        phone=54321,
        password="geladeira77",
    )


@pytest.fixture
def token_user2(db, client, user2):
    response = client.post(
        reverse("login"),
        data=json.dumps({"email": "user2@hotmail.com", "password": "geladeira77"}),
        content_type="application/json",
    )
    return ast.literal_eval(response.json().get("tokens"))["access"]


# Category
@pytest.fixture
def category(db, client):
    return Category.objects.create(name="Tecnologia")

@pytest.fixture
def base_64_image():
    with open("img_test.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        return str(my_string.decode("utf-8"))

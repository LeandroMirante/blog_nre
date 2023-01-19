from django.shortcuts import reverse
from rest_framework import status
import json


def test_register_user(client, db, base_64_image):
    payload = {
        "profile_picture": base_64_image,
        "email": "teste@teste.com",
        "name": "teste",
        "phone": "123456",
        "password": "geladeira55",
    }
    response = client.post(
        reverse("register"),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_login(client, user1):
    payload = {"email": "leandro.mirante@hotmail.com", "password": "geladeira55"}
    response = client.post(
        reverse("login"),
        data=payload,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK


def test_edit_user(client, user1, token_user1):
    payload = json.dumps({"email": "leandro.mirante@hotmail.com", "phone": 9999999})
    id = user1.id
    response = client.patch(
        f"/user/{id}/",
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    assert response.status_code == status.HTTP_200_OK


def test_user_can_edit_only_their_informations(client, user1, user2, token_user1):

    id_user1 = user1.id
    id_user2 = user2.id

    payload = json.dumps({"email": "leandro.mirante@hotmail.com", "phone": 9999999})

    # user1 editing user1 (can edit)
    response = client.patch(
        f"/user/{id_user1}/",
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    assert response.status_code == status.HTTP_200_OK

    # user1 editing user2 (can't edit)
    response = client.patch(
        f"/user/{id_user2}/",
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    assert response.status_code != status.HTTP_200_OK


def test_create_article(client, token_user1, category):
    payload = json.dumps(
        {"title": "Some Title", "category": 1, "description": "some description"}
    )
    response = client.post(
        reverse("article-create"),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    data = response.json()
    assert data["author"] == "Username 1"
    assert data["title"] == "Some Title"
    assert data["category"] == 1
    assert data["description"] == "some description"
    assert response.status_code == status.HTTP_201_CREATED

    reponse2 = client.get(
        reverse("article-detail", kwargs={"pk": 1}),
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    assert reponse2.json()["category"] == "Tecnologia"


def test_delete_article(client, user1, token_user1, token_user2, category):
    # Creating article using user1:
    category_id = category.id
    payload = json.dumps(
        {
            "title": "Some Title",
            "category": category_id,
            "description": "some description",
        }
    )
    response = client.post(
        reverse("article-create"),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )

    article_id = response.json()["id"]

    # test delete article using user2 (user2 can't delete the article)
    response = client.delete(
        reverse("article-delete", kwargs={"pk": article_id}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user2),
    )
    assert response.status_code != 204

    # test delete object using user1
    response = client.delete(
        reverse("article-delete", kwargs={"pk": article_id}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )

    assert response.status_code == 204

    # Verify that the object was deleted
    response = client.get(reverse("article-detail", kwargs={"pk": article_id}))
    assert response.status_code == 404


def test_only_article_author_can_edit_it(
    client, user1, user2, token_user1, token_user2, category
):
    # Creating article using user1:
    category_id = category.id
    payload = json.dumps(
        {
            "title": "Some Title",
            "category": category_id,
            "description": "some description",
        }
    )
    response = client.post(
        reverse("article-create"),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )

    article_id = response.json()["id"]

    # test edit article using user2 (user2 can't edit the article)
    payload = {"title": "Edited Title", "description": "Edited Category"}

    response = client.patch(
        reverse("article-update", kwargs={"pk": article_id}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user2),
    )
    assert response.status_code != status.HTTP_200_OK

    # test edit article using user1 (user1 can edit the article)
    payload = {"title": "Edited Title", "description": "Edited Category"}

    response = client.patch(
        reverse("article-update", kwargs={"pk": article_id}),
        content_type="application/json",
        data=payload,
        HTTP_AUTHORIZATION="Bearer {}".format(token_user1),
    )
    assert response.status_code == status.HTTP_200_OK

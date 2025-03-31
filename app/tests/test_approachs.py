from fastapi import status
from app.tests.test_users import create_user, login_user, user_create, psychologist_create

approach_create = {"name": "Cognitivo conductual"}

def test_read_approachs(client):
    response = client.get("/approachs")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_read_approach_by_id(client):
    response = client.post("/approachs", json=approach_create)
    approach_id = response.json()["approach_id"]
    response = client.get(f"/approachs/{approach_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == approach_create["name"]

def test_create_approach(client):
    response = client.post("/approachs", json=approach_create)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == approach_create["name"]

def test_update_approach(client):
    response = client.post("/approachs", json=approach_create)
    approach_id = response.json()["approach_id"]
    approach_update = {"name": "Cognitivo conductual modificado"}
    response = client.put(f"/approachs/{approach_id}", json=approach_update)

    assert response.status_code == status.HTTP_200_OK

def test_delete_approach(client):
    response = client.post("/approachs", json=approach_create)
    approach_id = response.json()["approach_id"]
    response = client.delete(f"/approachs/{approach_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

def post_approch_to_psychologist(client):
    response = client.post("/approachs", json=approach_create)
    approach_id = response.json()["approach_id"]
    create_user(client, user_create)
    token = login_user(client, user_create)
    response_create_psychologist = client.post("/users/psychologist", 
                                               json=psychologist_create, 
                                               headers=token)
    assert response_create_psychologist.status_code == status.HTTP_201_CREATED
    response = client.post(f"/approachs/psychologist/{approach_id}", headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["approach_id"] == approach_id




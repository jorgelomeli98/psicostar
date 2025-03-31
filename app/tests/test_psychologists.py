from app.tests.test_users import create_user, login_user, user_create, psychologist_create


def test_get_psychologists(client):
  
    response = client.get("/psychologists")
    assert response.status_code == 200

def test_read_psychologist_by_id(client):
    create_user(client, user_create)

    token = login_user(client, user_create)
    response = client.post("/users/psychologist",
                           json=psychologist_create,
                           headers=token)
    assert response.status_code == 201

    response = client.get(f"/psychologists/{response.json()['psychologist_id']}")
    assert response.status_code == 200

def test_read_psychologist_by_approach_id(client):
    create_user(client, user_create)
    response = client.post("/approachs",
                           json={"name": "Cognitivo Conductual"})
    assert response.status_code == 201
    assert response.json()["approach_id"] == 1
    approach_id = response.json()["approach_id"]

    token = login_user(client, user_create)
    response = client.post("/users/psychologist",
                           json=psychologist_create,
                           headers=token)
    assert response.status_code == 201
    print(type(approach_id))

    response = client.get(f"/psychologists/by-approach/{approach_id}")
    assert response.status_code == 200
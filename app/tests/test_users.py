from fastapi import status

user_create = {
    "name": "Pepe pecas", 
    "email": "example@example.com", 
    "tipo_usuario": "user", 
    "password": "1234"}

psychologist_create = {
    "cedula": "asdf", 
    "experiencia": "sassasa", 
    "ubicacion": "jksdlsjkdlsdj", 
    "approach_id": 1
}

def create_user(client, user):
    return client.post("/users", json=user)

def login_user(client, user):
    response = client.post("/users/login",
                       data={"username": user["email"],
                             "password": user["password"]})
    assert response.status_code == status.HTTP_202_ACCEPTED
    return {"Authorization": f"Bearer {response.json()["access_token"]}"}

def test_read_users(client):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK

def test_create_custumer(client):
    response = client.post(
        "/users", 
        json=user_create
    )

    assert response.status_code == status.HTTP_201_CREATED

def test_read_custumer(client):
    response = client.post(
        "/users", 
        json=user_create
    )

    assert response.status_code == status.HTTP_201_CREATED

    user_id = response.json()["user_id"]
    response_read = client.get(f"/users/{user_id}")

    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["email"] == "example@example.com"

def test_login_user(client):
    response = create_user(client, user_create)

    assert response.status_code == status.HTTP_201_CREATED

    response_login = client.post("/users/login", 
                                 data={"username": "example@example.com", 
                                       "password": "1234"})
    assert response_login.status_code == status.HTTP_202_ACCEPTED


def test_create_psychologist(client):
    create_user(client, user_create)

    token = login_user(client, user_create)

    response_create_psychologist = client.post("/users/psychologist", 
                                               json=psychologist_create, 
                                               headers=token)
    
    assert response_create_psychologist.status_code == status.HTTP_201_CREATED
    assert response_create_psychologist.json()["cedula"] == psychologist_create["cedula"]

def test_patch_user(client):
    create_user(client, user_create)

    token = login_user(client, user_create)

    response_patch = client.patch("/users",
                                  headers=token,
                                  json={"name": "Pepe pecotas"})
    
    assert response_patch.status_code == status.HTTP_200_OK


def test_delete_user(client):
    create_user(client, user_create)

    token = login_user(client, user_create)

    response_delete = client.delete("/users", headers=token)

    assert response_delete.status_code == status.HTTP_200_OK
    assert response_delete.json() == {"message": "Usuario eliminado"}

def test_read_all_users(client):
    create_user(client, user_create)

    token = login_user(client, user_create)

    response_read_all = client.get("/users", headers=token)

    assert response_read_all.status_code == status.HTTP_200_OK

def test_patch_psychologist(client):
    create_user(client, user_create)

    token = login_user(client, user_create)

    response_create_psychologist = client.post("/users/psychologist", 
                                               json=psychologist_create, 
                                               headers=token)
    
    assert response_create_psychologist.status_code == status.HTTP_201_CREATED
    assert response_create_psychologist.json()["cedula"] == psychologist_create["cedula"]

    response_patch_psychologist = client.patch("/users/psychologist", 
                                               headers=token, 
                                               json={"experiencia": "nueva experiencia"})

    assert response_patch_psychologist.status_code == status.HTTP_200_OK
    assert response_patch_psychologist.json()["experiencia"] == "nueva experiencia"




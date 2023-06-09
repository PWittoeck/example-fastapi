import pytest
from jose import jwt 
from App import schemas

from App.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello world."
#     assert res.status_code == 200       

def test_create_user(client):
    res = client.post("/users/", json={"email": "pwittoeck@gmail.com", "password": "Welkom01"})   
    # print(res.json())
    new_user =  schemas.UserOut(**res.json())
    # assert res.json().get("email") == ("pwittoeck@gmail.com")
    assert new_user.email == ("pwittoeck@gmail.com")
    assert res.status_code == 201                

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})   
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id =  payload.get("user_id") # type: ignore # 
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200




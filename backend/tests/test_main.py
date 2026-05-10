from .confest import client
from unittest.mock import patch


def test_login(client):
    response = client.post("/create_token", body={"email": "texetbuy@gmail.com", "password": "kiril12AZ"})
    assert response.status_code == 200
    assert response.json() == {"status": "oke"}



def test_bad_login(client):
    response = client.post("/create_token", body={"email": "wrong_email", "password": ""})
    assert response.status_code == 404
    assert response.json() == {"detail": "Email or password is incorrect"}




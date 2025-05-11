from fastapi.testclient import TestClient
from jose import jwt
from app import schemas
from app.config import settings
import pytest

# def test_root(client: TestClient):  # noqa: F811
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "Hello World!!!!!"
#     assert res.status_code == 200


def test_create_user(client: TestClient):  # noqa: F811
    res = client.post(
        "/users/", json={"email": "54yWZv@example.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "54yWZv@example.com"
    assert res.status_code == 201


def test_login_user(client: TestClient, test_user: schemas.UserOut):  # noqa: F811
    res = client.post(
        "/login",
        data={
            "username": test_user.get("email"),
            "password": test_user.get("password"),
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id: int = payload.get("user_id")  # Get as integer
    assert id == test_user.get("id")
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("54yWZv@example.com", "incorrect", 403),
    ("incorrect", "password123", 403),
    ("incorrect", "incorrect", 403),
    (None, "password123", 403),
    ("54yWZv@example.com", None, 403),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
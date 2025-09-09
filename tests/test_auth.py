from uuid import uuid4
import asyncio

from fastapi.testclient import TestClient
from tortoise import Tortoise
from main import app


def make_email() -> str:
    return f"user_{uuid4().hex}@example.com"


def setup_test_db():
    """테스트용 DB 초기화"""
    async def _init():
        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": ["app.models"]}
        )
        await Tortoise.generate_schemas()
    
    asyncio.run(_init())


def teardown_test_db():
    """테스트용 DB 정리"""
    async def _close():
        await Tortoise.close_connections()
    
    asyncio.run(_close())


def test_signup_success():
    setup_test_db()
    try:
        with TestClient(app) as client:
            email = make_email()
            resp = client.post(
                "/api/users/signup",
                json={"email": email, "password": "secret1234", "nickname": "neo"},
            )
            assert resp.status_code == 201, resp.text
            data = resp.json()
            assert data["email"] == email
            assert "id" in data
            assert "created_at" in data
    finally:
        teardown_test_db()


def test_signup_duplicate_email_returns_400():
    setup_test_db()
    try:
        with TestClient(app) as client:
            email = make_email()
            payload = {"email": email, "password": "secret1234"}
            r1 = client.post("/api/users/signup", json=payload)
            assert r1.status_code == 201
            r2 = client.post("/api/users/signup", json=payload)
            assert r2.status_code == 400
    finally:
        teardown_test_db()


def test_login_me_logout_flow():
    setup_test_db()
    try:
        with TestClient(app) as client:
            email = make_email()

            # signup
            r_signup = client.post("/api/users/signup", json={"email": email, "password": "pw123456"})
            assert r_signup.status_code == 201

            # login (OAuth2PasswordRequestForm)
            r_login = client.post(
                "/api/users/login",
                data={"username": email, "password": "pw123456"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert r_login.status_code == 200, r_login.text
            token = r_login.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # me
            r_me = client.get("/api/users/me", headers=headers)
            assert r_me.status_code == 200
            assert r_me.json()["email"] == email

            # logout -> token blacklisted
            r_logout = client.post("/api/users/logout", headers=headers)
            assert r_logout.status_code == 200

            # me with revoked token -> 401
            r_me2 = client.get("/api/users/me", headers=headers)
            assert r_me2.status_code == 401
    finally:
        teardown_test_db()


def test_login_with_wrong_password_returns_400():
    setup_test_db()
    try:
        with TestClient(app) as client:
            email = make_email()
            client.post("/api/users/signup", json={"email": email, "password": "pw123456"})
            r = client.post(
                "/api/users/login",
                data={"username": email, "password": "wrong"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert r.status_code == 400
    finally:
        teardown_test_db()

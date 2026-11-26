import json
import secrets
from pathlib import Path

from app.models.session import Session
from app.models.user import User


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def get_session(session_id: str) -> Session:
    with open(DATA_DIR / "sessions.json") as f:
        sessions = json.load(f)

    session = next(
        (s for s in sessions if s["session_id"] == session_id),
        None
    )

    if session is None:
        raise ValueError("Session not found")

    return Session(**session)


def get_user(user_id: str) -> User:
    with open(DATA_DIR / "users.json") as f:
        users = json.load(f)

    user = next(
        (u for u in users if u["user_id"] == user_id),
        None
    )

    if user is None:
        raise ValueError("User not found")

    return User(**user)


def get_user_from_session(session_id: str) -> User:
    session = get_session(session_id)
    return get_user(session.user_id)

def authenticate_user(username: str, password: str) -> User | None:
    with open(DATA_DIR / "users.json") as f:
        users = json.load(f)

    user = next(
        (
            u for u in users
            if u["username"] == username
            and u["password"] == password
        ),
        None
    )

    if user is None:
        return None

    return User(**user)

def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)

    with open(DATA_DIR / "sessions.json", "r") as f:
        sessions = json.load(f)

    sessions.append(
        {
            "session_id": session_id,
            "user_id": user_id,
        }
    )

    with open(DATA_DIR / "sessions.json", "w") as f:
        json.dump(sessions, f, indent=2)

    return session_id
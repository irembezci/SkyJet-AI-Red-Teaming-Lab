import json
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.services.auth_service import (
    authenticate_user,
    create_session,
    get_user_from_session,
)

from app.services.chatbot_service import chat


app = FastAPI(title="SkyJet AI")

templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    message: str


@app.post("/login")
def login(request: LoginRequest, response: Response):
    user = authenticate_user(
        request.username,
        request.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    session_id = create_session(user.user_id)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return {
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "username": user.username,
        },
    }

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )

@app.get("/me")
def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    user = get_user_from_session(session_id)

    return {
        "user_id": user.user_id,
        "name": user.name,
        "username": user.username,
    }


@app.post("/chat")
def chat_endpoint(
    request: Request,
    chat_request: ChatRequest
):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        response = chat(
            session_id=session_id,
            user_message=chat_request.message
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

    return {
        "response": response
    }

@app.post("/logout")
def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if session_id:
        # Remove the session from the local session store
        with open("data/sessions.json", "r") as f:
            sessions = json.load(f)

        sessions = [
            session
            for session in sessions
            if session["session_id"] != session_id
        ]

        with open("data/sessions.json", "w") as f:
            json.dump(sessions, f, indent=2)

    response.delete_cookie(
        key="session_id",
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return {"message": "Logout successful"}
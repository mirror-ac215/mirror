import json

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

PATIENT = {"Authorization": "Bearer dev-patient-token"}
CLINICIAN = {"Authorization": "Bearer dev-clinician-token"}
FRAME = {"image": ("frame.jpg", b"fake-jpeg-bytes", "image/jpeg")}


def client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def new_session(c: AsyncClient, consent: bool = True) -> str:
    response = await c.post("/sessions", json={"camera_consent": consent}, headers=PATIENT)
    assert response.status_code == 201
    return response.json()["session_id"]


@pytest.mark.anyio
async def test_login_gives_role_and_token() -> None:
    async with client() as c:
        response = await c.post(
            "/auth/login", json={"email": "clinician@demo.org", "password": "x"}
        )
    assert response.status_code == 200
    assert response.json()["role"] == "clinician"


@pytest.mark.anyio
async def test_sessions_need_a_token_401_and_a_patient_403() -> None:
    async with client() as c:
        no_token = await c.post("/sessions", json={"camera_consent": True})
        clinician = await c.post(
            "/sessions", json={"camera_consent": True}, headers=CLINICIAN
        )
    assert no_token.status_code == 401
    assert clinician.status_code == 403


@pytest.mark.anyio
async def test_frame_accepted_202_only_with_consent() -> None:
    async with client() as c:
        with_consent = await new_session(c, consent=True)
        without = await new_session(c, consent=False)
        ok = await c.post(f"/sessions/{with_consent}/frames", files=FRAME, headers=PATIENT)
        conflict = await c.post(f"/sessions/{without}/frames", files=FRAME, headers=PATIENT)
        unknown = await c.post("/sessions/nope/frames", files=FRAME, headers=PATIENT)
    assert ok.status_code == 202
    assert ok.json() == {"visual_status": "ok"}
    assert conflict.status_code == 409
    assert unknown.status_code == 404


@pytest.mark.anyio
async def test_message_streams_tokens_then_done() -> None:
    async with client() as c:
        session_id = await new_session(c)
        response = await c.post(
            f"/sessions/{session_id}/messages", json={"text": "hello"}, headers=PATIENT
        )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    events = []
    for block in response.text.strip().split("\n\n"):
        event_line, data_line = block.split("\n")
        name = event_line.removeprefix("event: ")
        data = json.loads(data_line.removeprefix("data: "))
        events.append((name, data))

    assert events[0][0] == "token"
    assert "text" in events[0][1]
    assert events[-1][0] == "done"
    assert events[-1][1]["context"]["tone_mode"] in ("coach", "supportive")
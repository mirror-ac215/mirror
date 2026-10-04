"""Login, sessions, frames and messages.

v0 stubs: the shapes follow the contract, the data is fake. The real CV call,
safety check, fusion and LLM call arrive in MS3.
"""

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.auth import demo_login, require_patient
from app.schemas import (
    FrameAck,
    LoginRequest,
    LoginResponse,
    MessageRequest,
    Session,
    SessionCreate,
)

# APIRouter groups related endpoints in their own file, which keeps main.py small. Main then plus in the router
router = APIRouter()

# In-memory store, lost on restart. The database replaces this later (M3-10).
sessions: dict[str, Session] = {}

STUB_REPLY = "Thanks for telling me that. What feels most important to talk about right now?"


def sse(event: str, data: dict) -> str:
    """One Server-Sent Event: an event name, a JSON data line, then a blank line."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def get_session(session_id: str) -> Session:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session")
    return session


@router.post("/auth/login")
def login(body: LoginRequest) -> LoginResponse:
    return demo_login(body.email)


@router.post("/sessions", status_code=201, dependencies=[Depends(require_patient)])
def start_session(body: SessionCreate) -> Session:
    session = Session(
        session_id=str(uuid4()),
        started_at=datetime.now(UTC),
        camera_consent=body.camera_consent,
    )
    sessions[session.session_id] = session
    return session

#run the patient check before this endpoint, if missing token gives 401 and a clinician gives 403
@router.post(
    "/sessions/{session_id}/frames",
    status_code=202,
    dependencies=[Depends(require_patient)],
)
async def receive_frame(session_id: str, image: UploadFile) -> FrameAck:
    session = get_session(session_id)
    if not session.camera_consent:
        raise HTTPException(status_code=409, detail="Camera consent was not given")
    await image.read()  # v0: read and discard. Frames are never stored.
    return FrameAck(visual_status="ok")


@router.post("/sessions/{session_id}/messages", dependencies=[Depends(require_patient)])
def send_message(session_id: str, body: MessageRequest) -> StreamingResponse:
    get_session(session_id)

    async def events() -> AsyncIterator[str]:
        for word in STUB_REPLY.split(" "):
            yield sse("token", {"text": word + " "})
            await asyncio.sleep(0.03)
        context = {
            "visual": {"status": "camera_off"},
            "text": {"top2": [["neutral", 0.6]]},
            "agreement": "n/a",
            "tone_mode": "coach",
            "note": "v0 stub: no real signals yet.",
        }
        yield sse("done", {"message_id": str(uuid4()), "context": context})

    return StreamingResponse(events(), media_type="text/event-stream")
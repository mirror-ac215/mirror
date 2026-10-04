""" Requests and response shapes from docs/contracts/api-gateway.openapi.yaml."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["patient", "clinician"]
VisualStatus = Literal["ok", "uncertain", "dropped", "camera_off"]

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    role: Role
    user_id: str

class SessionCreate(BaseModel):
    camera_consent: bool

class Session(BaseModel):
    session_id: str
    started_at: datetime
    camera_consent: bool

class FrameAck(BaseModel):
    visual_status: VisualStatus

class MessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
"""v0 stand-in for login. Real users, passwords and JWTs come in M4-02.

The token is a fixed string per role, so the flow (log in, send a Bearer token,
get 401/403) already works end to end, but nothing here is secure yet.
"""

from fastapi import Header, HTTPException

from app.schemas import LoginResponse, Role

DEMO_TOKENS: dict[str, Role] = {
    "dev-patient-token": "patient",
    "dev-clinician-token": "clinician",
}


def demo_login(email: str) -> LoginResponse:
    role: Role = "clinician" if "clinician" in email.lower() else "patient"
    token = "dev-clinician-token" if role == "clinician" else "dev-patient-token"
    user_id = "CL-01" if role == "clinician" else "MR-1087"
    return LoginResponse(access_token=token, role=role, user_id=user_id)


def current_role(authorization: str | None = Header(default=None)) -> Role:
    """401 if there is no valid token; otherwise the caller's role."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not logged in")
    role = DEMO_TOKENS.get(authorization.removeprefix("Bearer "))
    if role is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return role


def require_patient(authorization: str | None = Header(default=None)) -> Role:
    """403 if the caller is logged in but is not a patient."""
    role = current_role(authorization)
    if role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")
    return role
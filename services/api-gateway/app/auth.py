"""v0 stand-in for login. Real users, passwords and JWTs come in M4-02.

The token is a fixed string per role, so the flow (log in, send a Bearer token,
get 401/403) already works end to end, but nothing here is secure yet.
"""

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas import LoginResponse, Role

DEMO_TOKENS: dict[str, Role] = {
    "dev-patient-token": "patient",
    "dev-clinician-token": "clinician",
}

# Declares "Authorization: Bearer <token>" as a security scheme (the contract's
# bearerAuth). auto_error=False lets us return our own 401 message.
bearer = HTTPBearer(auto_error=False, scheme_name="bearerAuth")


def demo_login(email: str) -> LoginResponse:
    role: Role = "clinician" if "clinician" in email.lower() else "patient"
    token = "dev-clinician-token" if role == "clinician" else "dev-patient-token"
    user_id = "CL-01" if role == "clinician" else "MR-1087"
    return LoginResponse(access_token=token, role=role, user_id=user_id)


def current_role(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Role:
    """401 if there is no valid token; otherwise the caller's role."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    role = DEMO_TOKENS.get(credentials.credentials)
    if role is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return role


def require_patient(role: Annotated[Role, Depends(current_role)]) -> Role:
    """403 if the caller is logged in but is not a patient."""
    if role != "patient":
        raise HTTPException(status_code=403, detail="Patients only")
    return role
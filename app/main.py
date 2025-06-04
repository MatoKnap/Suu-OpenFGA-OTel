from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.otel import init_telemetry
import os
import requests


STORE_ID_EXTRACT_PATH = "/tmp/ids/openfga_store_id.txt"

app = FastAPI()

init_telemetry(service_name="openfga-python-client")

from app.fga_client import check_access, can_access

def get_store_id():
    try:
        with open(STORE_ID_EXTRACT_PATH) as f:
            return f.read().strip()
    except Exception:
        return os.getenv("OPENFGA_STORE_ID", "your_store_id_here")

OPENFGA_API_URL = os.getenv("OPENFGA_API_URL", "http://openfga:8080")
STORE_ID = get_store_id()

class PermissionRequest(BaseModel):
    """
    Request model for granting or revoking a permission.
    """
    user: str
    relation: str
    object: str


@app.get("/check")
async def check(user: str, resource: str):
    """
    Check if a user has access to a resource.
    - user: The user identifier (formula e.g., 'user:bob').
    - resource: The resource identifier (formula e.g., 'document:123').
    Returns whether the user is allowed.
    """
    allowed = check_access(user, resource)
    return {"allowed": allowed}


@app.post("/permissions/grant")
async def grant_permission(req: PermissionRequest):
    """
    Grant a permission to a user for a specific object and relation.
    """
    url = f"{OPENFGA_API_URL}/stores/{STORE_ID}/write"
    data = {
        "writes": {
            "tuple_keys": [
                {
                    "user": req.user,
                    "relation": req.relation,
                    "object": req.object
                }
            ]
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"OpenFGA error: {response.text}")
        # Increment the counter for Bob's access
    can_access.add(1, {"user": req.user, "relation": req.relation, "object": req.object})
    return {"status": "success"}


@app.post("/permissions/revoke")
async def revoke_permission(req: PermissionRequest):
    """
    Revoke a permission from a user for a specific object and relation.
    """
    url = f"{OPENFGA_API_URL}/stores/{STORE_ID}/write"
    data = {
        "deletes": {
            "tuple_keys": [
                {
                    "user": req.user,
                    "relation": req.relation,
                    "object": req.object
                }
            ]
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"OpenFGA error: {response.text}")
    can_access.add(-1, {"user": req.user, "relation": req.relation, "object": req.object})
    return {"status": "success"}
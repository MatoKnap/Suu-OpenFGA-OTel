import requests
from opentelemetry import trace
import os

tracer = trace.get_tracer(__name__)

FGA_API_URL = "http://openfga:8080"
STORE_NAME = "my-store"
STORE_ID = os.getenv("OPENFGA_STORE_ID", None)

if not STORE_ID:
    try:
        response = requests.get(f"{FGA_API_URL}/stores")
        response.raise_for_status()
        stores = response.json().get("stores", [])
        for store in stores:
            if store.get("name") == STORE_NAME:
                STORE_ID = store.get("id")
                break
    except requests.exceptions.RequestException as e:
        pass

def check_access(user, resource):
    with tracer.start_as_current_span("check_access"):
        response = requests.post(f"{FGA_API_URL}/stores/{STORE_ID}/check", json={
            "tuple_key": {
                "user": user,
                "relation": "can_access",
                "object": resource,
            }
        })
        return response.json().get("allowed", False)
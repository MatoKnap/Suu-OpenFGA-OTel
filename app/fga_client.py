import requests
from opentelemetry import trace
from opentelemetry import metrics
import os

meter = metrics.get_meter(__name__)
check_access_counter = meter.create_counter("check_access_calls", unit="1", description="Number of check access calls")

can_access = meter.create_up_down_counter(
    "can_access",
    description="Tracks if user can access a resource"
)
can_access.add(1, {"user": "user:alice", "relation":"can_access", "object": "document:123"})
can_access.add(0, {"user": "user:bob", "relation":"can_access", "object": "document:123"})

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
    # Ensure user is in the correct format
    if not user.startswith("user:"):
        user = f"user:{user}"
    with tracer.start_as_current_span("check_access"):
        response = requests.post(f"{FGA_API_URL}/stores/{STORE_ID}/check", json={
            "tuple_key": {
                "user": user,
                "relation": "can_access",
                "object": resource,
            }
        })
        span = trace.get_current_span()
        allowed = response.json().get("allowed", False)
        span.set_attribute("check.allowed", str(allowed))
        span.set_attribute("user", user)
        span.set_attribute("resource", resource)


        check_access_counter.add(1, {"allowed": str(allowed), "user": user, "resource": resource})

        return allowed

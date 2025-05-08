from fastapi import FastAPI
from app.fga_client import check_access
from app.otel import init_telemetry

app = FastAPI()

init_telemetry(service_name="openfga-python-client")

@app.get("/check")
async def check(user: str, resource: str):
    allowed = check_access(user, resource)
    return {"allowed": allowed}
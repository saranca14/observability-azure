import logging
import fastapi
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor
import os

# Ensure the environment variable is being accessed
connection_string = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING")
if not connection_string:
    raise ValueError("The APPLICATION_INSIGHTS_CONNECTION_STRING environment variable is not set correctly.")
print(f"Using connection string: {connection_string}")

# Configure Azure monitor collection telemetry pipeline
configure_azure_monitor(connection_string=connection_string)

app = fastapi.FastAPI()

# Requests made to fastapi endpoints will be automatically captured
@app.get("/")
async def test():
    return {"message": "Hello World"}

# Exceptions that are raised within the request are automatically captured
@app.get("/exception")
async def exception():
    raise Exception("Hit an exception")

# Set the OTEL_PYTHON_EXCLUDE_URLS environment variable to "http://127.0.0.1:8000/exclude"
# Telemetry from this endpoint will not be captured due to excluded_urls config above
#OTEL_PYTHON_EXCLUDE_URLS=http://127.0.0.1:8000/exclude
@app.get("/exclude")
async def exclude():
    return {"message": "Telemetry was not captured"}

if __name__ == "__main__":
    uvicorn.run("http_fastapi:app", port=8008, reload=True)

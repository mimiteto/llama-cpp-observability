import os
import logging

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import httpx
import traceback

app = FastAPI()
LLAMA_CPP_API_URL: str = os.environ.get("LLAMA_CPP_API_URL", "http://localhost:8080")
SD_HOST: str = os.environ.get("SD_HOST", "0.0.0.0")
SD_PORT: int = int(os.environ.get("SD_PORT", "6969"))

logging.basicConfig(level=logging.INFO)


@app.get("/")
async def root():
    return Response(
        content=f"""
LLaMA.cpp Observability API is running.
Targets discovery: <hr> <a href='/targets.json'>/targets.json</a>
Targets are discovered from {LLAMA_CPP_API_URL}/models endpoint. Only loaded models are included in the targets list.
""",
        media_type="text/html",
    )


@app.get("/targets.json")
async def get_targets():
    try:
        # Fetch models from the models endpoint
        async with httpx.AsyncClient() as client:
            try:
                models_response = await client.get(f"{LLAMA_CPP_API_URL}/models")
            except httpx.RequestError as e:
                logging.error(
                    f"Error fetching models from {LLAMA_CPP_API_URL}/models: {e}"
                )
                return JSONResponse([])
            models_data = models_response.json()

        # Parse models and find loaded ones
        targets = []
        for model in models_data.get("data", []):
            model_id = model["id"]
            status_value = model.get("status", {}).get("value", "")

            if status_value == "loaded":
                targets.append(
                    {
                        "targets": [LLAMA_CPP_API_URL.split("//")[-1]],
                        "labels": {
                            "llama_model_id": model_id,
                        },
                    }
                )

        return JSONResponse(targets)

    except Exception as e:
        # Return empty targets list on error to keep current targets
        traceback.print_exc()
        return JSONResponse([str(e)])


def main():
    import uvicorn

    uvicorn.run(app, host=SD_HOST, port=SD_PORT)


if __name__ == "__main__":
    main()

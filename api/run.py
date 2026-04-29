import os

import uvicorn


if __name__ == "__main__":
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", "8080"))
    uvicorn.run("api.app:app", host=host, port=port)

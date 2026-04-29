import uvicorn
from fastapi import FastAPI

from api.models import Command


app = FastAPI()


@app.post("/command", tags=["Команды"], summary="Передача новой команды серверу")
def put_command(command: str, time: float):
    putted_command = Command(
        message=command,
        time=time,
    )
    return {"message": f"Command '{putted_command.message}' executed successfully"}


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="localhost", port=8080)

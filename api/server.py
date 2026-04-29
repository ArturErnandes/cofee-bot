import uvicorn
from fastapi import FastAPI

from models import Command


app = FastAPI()


@app.post("/command", tags=["Команды"], summary="Передача новой команды серверу")
def put_command(command: str, time: float):
    command = Command(
        message=command,
        time=time,
    )
    return {"message": f"Command '{command.message}' executed successfully"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8080)
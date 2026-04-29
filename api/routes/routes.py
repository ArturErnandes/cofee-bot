from fastapi import APIRouter

from api.schemas.models import Command

router = APIRouter()


@router.post("/command", tags=["Команды"], summary="Передача новой команды серверу")
def put_command(command: str, time: float):
    putted_command = Command(
        message=command,
        time=time,
    )
    return {"message": f"Command '{putted_command.message}' executed successfully"}

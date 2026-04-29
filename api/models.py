from pydantic import BaseModel


class Command(BaseModel):
    message: str
    time: float

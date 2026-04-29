from fastapi import FastAPI

from api.routes.routes import router as commands_router

app = FastAPI()
app.include_router(commands_router)

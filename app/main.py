from fastapi import FastAPI
from app.routers import users, approachs, psychologists

app = FastAPI()

app.include_router(users.router, tags=["Users"])
app.include_router(approachs.router, tags=["Approachs"])
app.include_router(psychologists.router, tags=["Psychologists"])



@app.get("/")
async def root():
    return {"Message": "Bienvenido al sistema de rating de psicologos"}
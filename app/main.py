from fastapi import FastAPI
from app.routers import users, approachs

app = FastAPI()

app.include_router(users.router, tags=["Users"])
app.include_router(approachs.router, tags=["Approachs"])



@app.get("/")
async def root():
    return {"Message": "Bienvenido al sistema de rating de psicologos"}
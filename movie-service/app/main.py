from fastapi import FastAPI, Depends
from app.api.movies import movies
from app.api.db import metadata, database, engine
from app.api.auth import auth
from app.api.models import User

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth, prefix='/api/v1/auth', tags=['auth'])
app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])

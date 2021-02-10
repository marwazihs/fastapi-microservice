from typing import List
from fastapi import Header, APIRouter, HTTPException, Depends
from app.api.models import MovieIn, MovieOut, MovieUpdate, User
from app.api import db_manager
from app.api.auth import get_current_active_user


movies = APIRouter()


@movies.get('/', response_model=List[MovieOut] )
async def index(current_user: User = Depends(get_current_active_user)):
    return await db_manager.get_all_movies()


@movies.get('/{id}', response_model=MovieOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if movie:
        return movie
    raise HTTPException(status_code=404, detail="Movie with given id not found")


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response =  {
        'id': movie_id,
        **payload.dict()
        }
    return response


@movies.put('/{id}')
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    if movie:
        update_data = payload.dict(exclude_unset=True)

        if 'casts_id' in update_data:
            for cast_id in payload.casts_id:
                if not is_cast_present(cast_id):
                    raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

        movie_in_db = MovieIn(**movie)
        updated_movie = movie_in_db.copy(update=update_data)
        print(updated_movie)
        return await db_manager.update_movie(id, updated_movie)
        
    raise HTTPException(status_code=404, detail="Movie with given id not found")


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if movie:
        return await db_manager.delete_movie(id)
    raise HTTPException(status_code=404, detail="Movie with given id not found")

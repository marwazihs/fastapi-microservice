from typing import List, Optional
from pydantic import BaseModel


fake_movie_db = [
    {
        "name": "Star Wars: Episode IX - The Rise of Skywalker",
        "plot": "The surviving members of the resistance face the First Order once again.",
        "genres": ["Action", "Adventure", "Fantasy"],
        "casts": ["Daisy Ridley", "Adam Driver"]
    }
]
fake_users_db = [
    {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        }
    }
]

class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]

class MovieOut(MovieIn):
    id: int

class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class UserSignup(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None



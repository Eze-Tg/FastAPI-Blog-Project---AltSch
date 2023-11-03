from fastapi import APIRouter, Form, status, HTTPException
from typing import Annotated
from schemas.user_schema import User, CreateUser
from uuid import uuid4,UUID
from utils import get_hashed_password

users_routers = APIRouter()


db = [CreateUser(id = uuid4(), email= "theguys@gmail.com", username="Gee", first_name="Glan", last_name="Kemute", password="Mybugpass"), 
      CreateUser(id= uuid4(), email= "Emma@mail.com", username="hiri", first_name="Emmanu", last_name="Ohiri", password="@password"),
      CreateUser(id= uuid4(), email="badguy@mail.com", username="badguy", first_name="Bad", last_name="Guy", password="wosky")]


# @users_routers.get("/{user_id}")
# def get_user_by_id(self, users: list[db], user_id):
#     for user in users:
#         if user.id == user_id:
#             return user
#     return{"error": "User not found"}


#Register new User
@users_routers.post("/signup/", summary="Create New User")
async def signup(
    username: Annotated[str, Form()],
    firstname: Annotated[str, Form()],
    lastname: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    #querrying the db to check if user already exist
    for user in db:
        if user.username == username:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    new_user = CreateUser(
        id=str(UUID(int=len(db) +1)),
        username=username, 
        first_name=firstname, 
        last_name=lastname,
        email=email,
        password=get_hashed_password(password))
    db.append(new_user)
    return{"message": "Welcome", "Your username is": new_user.username}


#Login route
@users_routers.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    for items in db:
        if items.username == username and items.password == password:
            return{"message": "You have been logged in succesfully!"}
    return{"message": "Username or password incorrect!"}


#Get all users
@users_routers.get("/")
def fetch_users():
    return db
    

#Delete user
@users_routers.delete("/{user_id}")
def delete_user(user_id: uuid4):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return db


from fastapi import APIRouter
from schemas.user_schema import User, CreateUser
from uuid import uuid4

users_routers = APIRouter()

# db: list[User] = [
#     User(
#         id=uuid4(), 
#         email = "yakubsjohn@mail.com",
#         first_name="Johnson", 
#         last_name="Yakubu", 
#         Gender="male"
#         ),
#         User(
#         id=uuid4(), 
#         email = "ritaevenling@mail.com",
#         first_name="Rita", 
#         last_name="Eveline", 
#         Gender="female"
#         ),
# ]




db = [User(id = uuid4(), email= "theguys@gmail.com", name="Gee"), 
      User(id= uuid4(), email= "Emma@mail.com", name="Ohiri")]


@users_routers.get("/")
def fetch_users():
    return db


# @users_routers.get("/{user_id}")
# def get_user_by_id(self, users: list[db], user_id):
#     for user in users:
#         if user.id == user_id:
#             return user
#     return{"error": "User not found"}


#Register new user
@users_routers.post("/sign_up")
def sign_up(user: CreateUser, email, first_name, last_name, gender):
    user.id = uuid4()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.gender = gender
    db.append(user)
    return{'id': user.id, "user_email": email}


#Delete user
@users_routers.delete("/{user_id}")
def delete_user(user_id: uuid4):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return db


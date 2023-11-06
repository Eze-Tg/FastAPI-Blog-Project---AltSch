from fastapi import APIRouter, Form, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Annotated
from schemas.user_schema import User, CreateUser
from uuid import uuid4,UUID
from utils import (get_hashed_password, 
                   create_access_token, 
                   verify_password)


users_routers = APIRouter()


db = [CreateUser(id = uuid4(), email= "theguys@gmail.com", username="Gee", first_name="Glan", last_name="Kemute", password="Mybugpass", access_token=""), 
      CreateUser(id= uuid4(), email= "Emma@mail.com", username="hiri", first_name="Emmanu", last_name="Ohiri", password="@password", access_token=""),
      CreateUser(id= uuid4(), email="badguy@mail.com", username="badguy", first_name="Bad", last_name="Guy", password="wosky", access_token="")]



def find_username(database, input_username):
    for item in database:
        if item.username == input_username:
            return item
    return{"message" : "user not found!"}

def get_username_from_token(input_token):
    for item in db:
        if item.access_token == input_token:
            return item.username
    return False


# for items in db:
#         print(items.email)

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

    # if user is not None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exist"
    #     )

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
@users_routers.post("/login", summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = ''

    username_check = find_username(db, form_data.username)

    if username_check != None:
        user_pass = username_check.password
        if not verify_password(form_data.password, user_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password")
        # if form_data.password == user_pass:
        token = create_access_token(username_check.id)
        username_check.access_token = token
        return {"message" : "Correct Details, User is logged in!", "token": token }

        
        

        # hashed_password = 

        print(username_check)
        print("Success!!")
        return{"message": "login succesful!"}


    
        # detail="Incorrect email or password")
        
    # hashed_pass = db['password']
    # if not verify_password(form_data.password, hashed_pass):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect email or password")
    
    # return{
    #     "access_token": create_access_token(user),
    #     "refresh_token": create_refresh_token(user)
    # }


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


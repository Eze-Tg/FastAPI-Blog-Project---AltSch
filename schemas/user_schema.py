from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum


#This section defines the data models that would be used for the user data validation

class Gender(str, Enum):
    male = "male",
    female = "female"



class CreateUser(BaseModel):
    id: Optional[UUID] = uuid4()
    email: str
    first_name: str
    last_name: str
    username: str
    password: str
    access_token: Optional[str] = None




class User(BaseModel):
    id: Optional[UUID] = uuid4()
    email: str
    name: str


class UserLogin(BaseModel):
    email:str
    password: str
    access_token: Optional[str] = None



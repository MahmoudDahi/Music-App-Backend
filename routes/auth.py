from fastapi import APIRouter, HTTPException
from database import db
from models.user import User
from pydantic_schemas.user_create import UserCreate

import uuid
import bcrypt

router = APIRouter()

@router.post('/signup')
def signup_user(user:UserCreate):
    #check if user exist in DB
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(400,'User with same Email Already Exist') 
    
    #hash password
    hash_pw = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    db_user = User(id= str(uuid.uuid4()),name=user.name,email=user.email,password=hash_pw)
    db.add(db_user)
    db.commit()
    return 'User created'
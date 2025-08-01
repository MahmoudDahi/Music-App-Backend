from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin

import uuid
import bcrypt


router = APIRouter()

@router.post('/signup',status_code=201)
def signup_user(user:UserCreate,db: Session= Depends(get_db)):
    #check if user exist in DB
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(400,'User with same Email Already Exist') 
    #hash password
    hash_pw = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    db_user = User(id= str(uuid.uuid4()),name=user.name,email=user.email,password=hash_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post('/login')
def login_user(user:UserLogin,db: Session= Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(400,'User with this email does not exist')
    if not bcrypt.checkpw(user.password.encode(),db_user.password):
        raise HTTPException(400,'Incorrect Password')
    return db_user
    

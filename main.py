from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
from models import model_git_info, model_stack, model_user
from schemas import schema_git_info, schema_stack, schema_user
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")

    model_user = crud.create_user(db=db, user=user)
    print(model_user.is_active)
    user = schema_user.UserResponse(name=model_user.name, group=model_user.group, email=model_user.email, is_active=model_user.is_active)
    return user


@app.get("/users/", response_model=List[schema_user.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    model_users = crud.get_users(db, skip=skip, limit=limit)
    schema_users = []
    for model_user in model_users:
        user = schema_user.UserResponse(name=model_user.name, group=model_user.group, email=model_user.email, is_active=model_user.is_active)
        schema_users.append(user)
    return schema_users


@app.get("/users/{user_id}", response_model=schema_user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    model_user = crud.get_user(db, user_id=user_id)
    if model_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = schema_user.UserResponse(name=model_user.name, group=model_user.group, email=model_user.email, is_active=model_user.is_active)
    return user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
# 
# 
# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
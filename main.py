# 標準ライブラリ
from typing import List
# 3rdPartyライブラリ
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# ローカルファイル
import crud
from models import model_git_info, model_stack, model_user
from schemas import schema_git_info, schema_stack, schema_user
from database import SessionLocal, engine, Base
from password_crypter import PasswordCrypter
from token_generator import TokenGenerator

ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@admin.com"
ADMIN_PASSWORD="password"


# DB初期化
Base.metadata.create_all(bind=engine)


# アプリ起動
app = FastAPI()

# OAuth2有効化
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# DI用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 初期データ登録
@app.on_event("startup")
def insert_initial_data():
    print("初期ユーザー(Admin)生成開始")
    # adminユーザー作成
    db = SessionLocal()
    admin = crud.get_user_by_name(db, name="admin")
    # 既に存在する場合はスキップ
    if admin:
        return
    hashed_password = PasswordCrypter.get_hash(password=ADMIN_PASSWORD)
    db_user = model_user.User(email=ADMIN_EMAIL, hashed_password=hashed_password, name=ADMIN_USERNAME, is_active=True, is_admin=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return

# 共通処理
def check_token(token: str, db: Session, only_admin=False):
    name = TokenGenerator.get_username_from_token(token)
    db_user = crud.get_user_by_name(db, name=name)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    if only_admin:
        if not db_user.is_admin:
            raise HTTPException(status_code=400, detail="This Action is only allowed for admin user")


# API定義
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # ユーザーが存在するか確認
    db_user = crud.get_user_by_name(db, name=form_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorecct username or password")

    # パスワードが一致しているか確認
    if not PasswordCrypter.verify(hashed_password=db_user.hashed_password, plain_password=form_data.password):
        raise HTTPException(status_code=400, detail="Incorecct username or password")
    
    access_token = TokenGenerator.generate_token(data={"sub": db_user.name,})
    return {"access_token": access_token, "token_type": "bearer"}

    
@app.post("/users/", response_model=schema_user.UserResponse)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # トークン確認
    check_token(token, db, only_admin=True)

    # 既に登録済みのE-Mailか確認
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 既に登録済みのユーザー名か確認
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")

    # ユーザー登録
    model_user = crud.create_user(db=db, user=user)
    user = schema_user.UserResponse(name=model_user.name, group=model_user.group, email=model_user.email, is_active=model_user.is_active)
    return user


@app.get("/users/", response_model=List[schema_user.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # トークン確認
    check_token(token, db, only_admin=True)

    # ユーザー一覧取得
    model_users = crud.get_users(db, skip=skip, limit=limit)
    schema_users = []
    for model_user in model_users:
        user = schema_user.UserResponse(name=model_user.name, email=model_user.email, is_active=model_user.is_active, is_admin=model_user.is_admin)
        schema_users.append(user)
    return schema_users
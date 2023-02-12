from sqlalchemy.orm import Session

from models import model_git_info, model_stack, model_user
from schemas import schema_git_info, schema_stack, schema_user


def get_user(db: Session, user_id: int):
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    # return db.query(schema_user.User).filter(schema_user.User.email == email).first()
    return db.query(model_user.User).filter(model_user.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(model_user.User).filter(model_user.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema_user.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = model_user.User(email=user.email, hashed_password=fake_hashed_password, group=0, name=user.name, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.git_info = create_git_info(db=db, git_info=model_git_info.GitInfo(), user_id=db_user.id);
    db.commit()
    db.refresh(db_user)
    return db_user

def create_git_info(db: Session, git_info: schema_git_info.GitInfo, user_id: int, git_name="", git_email="", gitlab_token="",):
    db_git_info = model_git_info.GitInfo(git_name=git_name, git_email=git_email, gitlab_token=gitlab_token, owner_id=user_id)
    db.add(db_git_info)
    db.commit()
    db.refresh(db_git_info)
    return db_git_info


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(model.Item).offset(skip).limit(limit).all()
# 
# 
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
from sqlalchemy.orm import Session
from .. import models, schemas, hashing
from fastapi import HTTPException, status


def create_user(req: schemas.User, db: Session):
    hashed_pwd = hashing.Hash.bcrypt(req.password)
    new_user = models.User(name=req.name, email=req.email,
                           password=hashed_pwd, role=req.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    return user


def get_all_users(db: Session):
    return db.query(models.User).all()

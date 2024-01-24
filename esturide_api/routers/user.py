from re import search
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from esturide_api import models, oauth2, schemas, utils
from esturide_api.config.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        return new_user

    except IntegrityError as e:
        error_str = str(e)
        if search("UNIQUE constraint failed: users.email", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        elif search("UNIQUE constraint failed: users.curp", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CURP already registered",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    users = db.query(models.User).all()
    print(current_user.email)
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist",
        )

    return user


@router.put("/{id}", response_model=schemas.UserOut)
def update_user_put(
    id: int,
    updated_user: schemas.UserUpdatePut,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    try:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )

        user_query.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return user_query.first()
    except IntegrityError as e:
        error_str = str(e)
        if search("UNIQUE constraint failed: users.email", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        elif search("UNIQUE constraint failed: users.curp", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CURP already registered",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.patch("/{id}", response_model=schemas.UserOut)
def update_user_patch(
    id: int,
    updated_user: schemas.UserUpdatePatch,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    try:
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )

        user_attributes = [attr.name for attr in models.User.__table__.columns]

        for attribute in user_attributes:
            if (
                hasattr(updated_user, attribute)
                and getattr(updated_user, attribute) is not None
            ):
                setattr(user, attribute, getattr(updated_user, attribute))

        db.commit()
        db.refresh(user)
        return user_query.first()
    except IntegrityError as e:
        error_str = str(e)
        if search("UNIQUE constraint failed: users.email", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        elif search("UNIQUE constraint failed: users.curp", error_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CURP already registered",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    user.delete(synchronize_session=False)
    db.commit()
    return {"message": f"User with id {id} was successfully deleted"}

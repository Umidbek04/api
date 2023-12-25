from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import database, models, utils, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get('/', response_model=list[schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users



@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def make_user(user: schemas.UserMake, db: Session = Depends(get_db)):

    hashed_password = utils.pwd_context.hash(user.password)
    new_user = models.User(email = user.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user



@router.get("/{id}")
def get_user_id(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    response_data = schemas.UserResponse(
        email=get_user.email,
        id = get_user.id,
        made_time=get_user.made_time
    )
    return response_data


# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_user(id: int, db: Session = Depends(get_db)):
    
#     deleted_user = db.query(models.User).filter(models.User.id == id).first()

#     if not deleted_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id}, does not exist")
    
#     db.delete(deleted_user)
#     db.commit()
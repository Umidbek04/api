from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, utils, schemas, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    

    access_token = oauth2.make_access_token(data={"id": user.id})

    return {"token":access_token, "token_type":"bearer"}


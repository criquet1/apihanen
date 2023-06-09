from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

  user =  db.query(models.User).filter(models.User.user_email == user_credentials.username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials 1")

  if not utils.verify(user_credentials.password, user.user_password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials 2")

  access_token = oauth2.create_access_token(data = {"user_id": user.user_id})
  
  return {"access_token": access_token, "token_type": "bearer" }
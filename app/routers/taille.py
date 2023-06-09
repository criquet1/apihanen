from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/tailles",
  tags=['Tailles']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Taille])
def get_tailles(db: Session = Depends(get_db)):
  tailles = db.query(models.Taille).all()
  return tailles 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Taille)
def get_taille(id: int, db: Session = Depends(get_db)):

  taille = db.query(models.Taille).filter(models.Taille.id == id).first()

  if not taille:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"taille with id: {id} was not found")
  return taille

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Taille)
def create_taille(taille: schemas.Taille_create, db: Session = Depends(get_db)):

  new_taille = models.Taille(**taille.dict())
  db.add(new_taille)
  db.commit()
  db.refresh(new_taille)

  return new_taille

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_taille(id:int, db: Session = Depends(get_db)):
  taille = db.query(models.Taille).filter(models.Taille.id == id)

  if taille.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"taille with id: {id} does not exist")
  
  taille.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Taille)
def update_taille(id: int, updated_taille: schemas.Taille_create, db: Session = Depends(get_db)):

  taille_query = db.query(models.Taille).filter(models.Taille.id == id)
  taille = taille_query.first()

  if taille == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"taille with id: {id} does not exist")
  
  taille_query.update(updated_taille.dict(), synchronize_session=False)

  db.commit()

  return taille_query.first()

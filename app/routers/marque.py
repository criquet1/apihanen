from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/marques",
  tags=['Marques']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Marque])
def get_marques(db: Session = Depends(get_db)):
  marques = db.query(models.Marque).all()
  return marques 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Marque)
def get_marque(id: int, db: Session = Depends(get_db)):

  marque = db.query(models.Marque).filter(models.Marque.id == id).first()

  if not marque:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"marque with id: {id} was not found")
  return marque

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Marque)
def create_marque(marque: schemas.Marque_create, db: Session = Depends(get_db)):

  new_marque = models.Marque(**marque.dict())
  db.add(new_marque)
  db.commit()
  db.refresh(new_marque)

  return new_marque

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marque(id:int, db: Session = Depends(get_db)):
  marque = db.query(models.Marque).filter(models.Marque.id == id)

  if marque.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"marque with id: {id} does not exist")
  
  marque.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Marque)
def update_marque(id: int, updated_marque: schemas.Marque_create, db: Session = Depends(get_db)):

  marque_query = db.query(models.Marque).filter(models.Marque.id == id)
  marque = marque_query.first()

  if marque == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"marque with id: {id} does not exist")
  
  marque_query.update(updated_marque.dict(), synchronize_session=False)

  db.commit()

  return marque_query.first()

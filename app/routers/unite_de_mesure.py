from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/unites_de_mesure",
  tags=['Unités de mesure']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Unite_de_mesure])
def get_unites_de_mesure(db: Session = Depends(get_db)):
  unites_de_mesure = db.query(models.Unite_de_mesure).all()
  return unites_de_mesure 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Unite_de_mesure)
def get_unite_de_mesure(id: int, db: Session = Depends(get_db)):

  unite_de_mesure = db.query(models.Unite_de_mesure).filter(models.Unite_de_mesure.id == id).first()

  if not unite_de_mesure:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"unite_de_mesure with id: {id} was not found")
  return unite_de_mesure

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Unite_de_mesure)
def create_unite_de_mesure(unite_de_mesure: schemas.Unite_de_mesure_create, db: Session = Depends(get_db)):

  new_unite_de_mesure = models.Unite_de_mesure(**unite_de_mesure.dict())
  db.add(new_unite_de_mesure)
  db.commit()
  db.refresh(new_unite_de_mesure)

  return new_unite_de_mesure

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unite_de_mesure(id:int, db: Session = Depends(get_db)):
  unite_de_mesure = db.query(models.Unite_de_mesure).filter(models.Unite_de_mesure.id == id)

  if unite_de_mesure.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"unité de mesure with id: {id} does not exist")
  
  unite_de_mesure.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Unite_de_mesure)
def update_unite_de_mesure(id: int, updated_unite_de_mesure: schemas.Unite_de_mesure_create, db: Session = Depends(get_db)):

  unite_de_mesure_query = db.query(models.Unite_de_mesure).filter(models.Unite_de_mesure.id == id)
  unite_de_mesure = unite_de_mesure_query.first()

  if unite_de_mesure == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"unite_de_mesure with id: {id} does not exist")
  
  unite_de_mesure_query.update(updated_unite_de_mesure.dict(), synchronize_session=False)

  db.commit()

  return unite_de_mesure_query.first()

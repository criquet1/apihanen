from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/clienteles",
  tags=['Clienteles']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Clientele])
def get_clienteles(db: Session = Depends(get_db)):
  clienteles = db.query(models.Clientele).all()
  return clienteles 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Clientele)
def get_clientele(id: int, db: Session = Depends(get_db)):

  clientele = db.query(models.Clientele).filter(models.Clientele.id == id).first()

  if not clientele:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"clientele with id: {id} was not found")
  return clientele

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Clientele)
def create_clientele(clientele: schemas.Clientele_create, db: Session = Depends(get_db)):

  new_clientele = models.Clientele(**clientele.dict())
  db.add(new_clientele)
  db.commit()
  db.refresh(new_clientele)

  return new_clientele

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clientele(id:int, db: Session = Depends(get_db)):
  clientele = db.query(models.Clientele).filter(models.Clientele.id == id)

  if clientele.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"clientele with id: {id} does not exist")
  
  clientele.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Clientele)
def update_clientele(id: int, updated_clientele: schemas.Clientele_create, db: Session = Depends(get_db)):

  clientele_query = db.query(models.Clientele).filter(models.Clientele.id == id)
  clientele = clientele_query.first()

  if clientele == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"clientele with id: {id} does not exist")
  
  clientele_query.update(updated_clientele.dict(), synchronize_session=False)

  db.commit()

  return clientele_query.first()

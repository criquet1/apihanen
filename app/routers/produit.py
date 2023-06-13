from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/produits",
  tags=['Produits']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Produit])
def get_produits(db: Session = Depends(get_db)):
  produits = db.query(models.Produit).all()
  return produits 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Produit)
def get_produit(id: int, db: Session = Depends(get_db)):

  produit = db.query(models.Produit).filter(models.Produit.id == id).first()

  if not produit:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"produit with id: {id} was not found")
  return produit

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Produit)
def create_produit(produit: schemas.Produit_create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  new_produit = models.Produit(**produit.dict())
  db.add(new_produit)
  db.commit()
  db.refresh(new_produit)

  return new_produit

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produit(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  produit = db.query(models.Produit).filter(models.Produit.id == id)

  if produit.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"produit with id: {id} does not exist")
  
  produit.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Produit)
def update_produit(id: int, updated_produit: schemas.Produit_create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  produit_query = db.query(models.Produit).filter(models.Produit.id == id)
  produit = produit_query.first()

  if produit == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"produit with id: {id} does not exist")
  
  produit_query.update(updated_produit.dict(), synchronize_session=False)

  db.commit()

  return produit_query.first()

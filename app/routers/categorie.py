from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/categories",
  tags=['Categories']
)

# ***************************************************************


@router.get("/", response_model=List[schemas.Categorie])
def get_categories(db: Session = Depends(get_db)):
  categories = db.query(models.Categorie).all()
  return categories 

# ***************************************************************


@router.get("/{id}", response_model=schemas.Categorie)
def get_categorie(id: int, db: Session = Depends(get_db)):

  categorie = db.query(models.Categorie).filter(models.Categorie.id == id).first()

  if not categorie:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"categorie with id: {id} was not found")
  return categorie

# ***************************************************************


@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Categorie)
def create_categorie(categorie: schemas.Categorie_create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  new_categorie = models.Categorie(**categorie.dict())
  db.add(new_categorie)
  db.commit()
  db.refresh(new_categorie)

  return new_categorie

# ***************************************************************


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categorie(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  categorie = db.query(models.Categorie).filter(models.Categorie.id == id)

  if categorie.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"categorie with id: {id} does not exist")
  
  categorie.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ***************************************************************


@router.put("/{id}", response_model=schemas.Categorie)
def update_categorie(id: int, updated_categorie: schemas.Categorie_create, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  categorie_query = db.query(models.Categorie).filter(models.Categorie.id == id)
  categorie = categorie_query.first()

  if categorie == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"categorie with id: {id} does not exist")
  
  categorie_query.update(updated_categorie.dict(), synchronize_session=False)

  db.commit()

  return categorie_query.first()

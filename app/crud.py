from sqlalchemy.orm import Session
from . import schemas
from . import models


def get_facture(db: Session, facture_id: int):
    return db.query(models.Facture).filter(models.Facture.id == facture_id).first()


def get_facture_by_fact_id(db: Session, fact_id: str):
    return db.query(models.Facture).filter(models.Facture.id == fact_id).first()


def get_factures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Facture).order_by(models.Facture.date.desc()).offset(skip).limit(limit).all()


def create_facture(db: Session, facture: schemas.FactureCreate):
    new_facture = models.Facture(**facture.dict())
    db.add(new_facture)
    db.commit()
    # similaire à returning *, après le commit le id est disponible
    db.refresh(new_facture)
    return new_facture


from sqlalchemy import Date, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship, backref


class Categorie(Base):
  __tablename__ = "categories"
  id = Column(Integer, primary_key=True, nullable=False)
  nom = Column(String(40), nullable=False)
  descr = Column(String(200), nullable=False)
  image_url = Column(String(40), nullable=False)


class Clientele(Base):
  __tablename__ = "clienteles"
  id = Column(Integer, primary_key=True, nullable=False)
  nom = Column(String(50), nullable=False)


class Marque(Base):
  __tablename__ = "marques"
  id = Column(Integer, primary_key=True, nullable=False)
  nom = Column(String(50), nullable=False)


class Unite_de_mesure(Base):
  __tablename__ = "unites_de_mesure"
  id = Column(Integer, primary_key=True, nullable=False)
  nom = Column(String(50), nullable=False)


class Taille(Base):
  __tablename__ = "tailles"
  id = Column(Integer, primary_key=True, nullable=False)
  nom = Column(String(50), nullable=False)


class Produit(Base):
  __tablename__ = "produits"
  id = Column(Integer, primary_key=True, nullable=False)
  categorie_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
  categorie = relationship("Categorie")
  clientele_id = Column(Integer, ForeignKey("clienteles.id", ondelete="CASCADE"), nullable=False, default=0)
  clientele = relationship("Clientele")
  marque_id = Column(Integer, ForeignKey("marques.id", ondelete="CASCADE"), nullable=False, default=0)
  marque = relationship("Marque")
  unite_de_mesure_id = Column(Integer, ForeignKey("unites_de_mesure.id", ondelete="CASCADE"), nullable=True, default=0)
  unite_de_mesure = relationship("Unite_de_mesure")
  taille_id = Column(Integer, ForeignKey("tailles.id", ondelete="CASCADE"), nullable=True, default=0)
  taille = relationship("Taille")
  format = Column(Float, nullable=True)
  nom = Column(String(40), nullable=False)
  descr = Column(String(200), nullable=False)
  image_url = Column(String(40), nullable=False)
  quantite_inv = Column(Float, nullable=True)
  prix_vente = Column(Float, nullable=True)
  prix_achat = Column(Float, nullable=True)
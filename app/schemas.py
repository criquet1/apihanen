from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from pydantic.types import conint
from typing import Optional, List


class UserBase(BaseModel):
  user_email: EmailStr
  user_password: str

class UserCreate(UserBase):
  pass

class User(BaseModel):
  user_id: int
  user_email: EmailStr

  class Config:
    orm_mode = True


class Categorie(BaseModel):
  id: int
  nom: str
  descr: str
  image_url: str

  class Config:
      orm_mode = True


class Categorie_create(BaseModel):
  nom: str
  descr: str
  image_url: str

  class Config:
      orm_mode = True


class Clientele(BaseModel):
  id: int
  nom: str

  class Config:
      orm_mode = True


class Clientele_create(BaseModel):
  nom: str

  class Config:
      orm_mode = True

class Marque(BaseModel):
  id: int
  nom: str

  class Config:
      orm_mode = True


class Marque_create(BaseModel):
  nom: str

  class Config:
      orm_mode = True

class Taille(BaseModel):
  id: int
  nom: str

  class Config:
      orm_mode = True


class Taille_create(BaseModel):
  nom: str

  class Config:
      orm_mode = True


class Unite_de_mesure(BaseModel):
  id: int
  nom: str

  class Config:
      orm_mode = True


class Unite_de_mesure_create(BaseModel):
  nom: str

  class Config:
      orm_mode = True


class Produit(BaseModel):
  id: int
  categorie: Categorie
  clientele: Clientele
  marque: Marque
  unite_de_mesure: Unite_de_mesure
  taille: Taille
  format: float
  nom: str
  descr: str
  image_url: str
  quantite_inv: float
  prix_vente: float
  prix_achat: float

  class Config:
      orm_mode = True


class Produit_create(BaseModel):
  categorie_id: int
  clientele_id: int
  marque_id: int
  unite_de_mesure_id: int
  taille_id: int
  format: float
  nom: str
  descr: str
  image_url: str
  quantite_inv: float
  prix_vente: float
  prix_achat: float

  class Config:
      orm_mode = True
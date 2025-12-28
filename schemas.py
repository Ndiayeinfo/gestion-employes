from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Schéma pour la création d'un employé
class EmployeCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: Optional[str] = None
    poste: str
    salaire: Optional[float] = None
    date_embauche: Optional[date] = None
    departement: Optional[str] = None

# Schéma pour la mise à jour d'un employé
class EmployeUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    poste: Optional[str] = None
    salaire: Optional[float] = None
    date_embauche: Optional[date] = None
    departement: Optional[str] = None

# Schéma pour la réponse (affichage)
class EmployeResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    telephone: Optional[str]
    poste: str
    salaire: Optional[float]
    date_embauche: Optional[date]
    departement: Optional[str]
    
    class Config:
        from_attributes = True


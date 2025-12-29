from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime

# Schéma pour la création d'un employé
class EmployeCreate(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100, description="Nom de l'employé (1-100 caractères)")
    prenom: str = Field(..., min_length=1, max_length=100, description="Prénom de l'employé (1-100 caractères)")
    email: EmailStr = Field(..., description="Email de l'employé (doit être unique)")
    telephone: Optional[str] = Field(None, max_length=20, description="Numéro de téléphone (max 20 caractères)")
    poste: str = Field(..., min_length=1, max_length=100, description="Poste occupé (1-100 caractères)")
    salaire: Optional[float] = Field(None, gt=0, description="Salaire (doit être positif)")
    date_embauche: Optional[date] = Field(None, description="Date d'embauche (format: YYYY-MM-DD)")
    departement: Optional[str] = Field(None, max_length=100, description="Département (max 100 caractères)")
    
    @field_validator('nom', 'prenom', 'poste')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Valide que les champs ne sont pas vides ou ne contiennent que des espaces"""
        if not v or not v.strip():
            raise ValueError("Ce champ ne peut pas être vide")
        return v.strip()
    
    @field_validator('salaire')
    @classmethod
    def validate_salaire_positif(cls, v: Optional[float]) -> Optional[float]:
        """Valide que le salaire est positif"""
        if v is not None and v <= 0:
            raise ValueError("Le salaire doit être un nombre positif")
        return v
    
    @field_validator('date_embauche')
    @classmethod
    def validate_date_embauche(cls, v: Optional[date]) -> Optional[date]:
        """Valide que la date d'embauche n'est pas dans le futur"""
        if v is not None:
            today = date.today()
            if v > today:
                raise ValueError("La date d'embauche ne peut pas être dans le futur")
        return v

# Schéma pour la mise à jour d'un employé
class EmployeUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=1, max_length=100, description="Nom de l'employé (1-100 caractères)")
    prenom: Optional[str] = Field(None, min_length=1, max_length=100, description="Prénom de l'employé (1-100 caractères)")
    email: Optional[EmailStr] = Field(None, description="Email de l'employé (doit être unique)")
    telephone: Optional[str] = Field(None, max_length=20, description="Numéro de téléphone (max 20 caractères)")
    poste: Optional[str] = Field(None, min_length=1, max_length=100, description="Poste occupé (1-100 caractères)")
    salaire: Optional[float] = Field(None, gt=0, description="Salaire (doit être positif)")
    date_embauche: Optional[date] = Field(None, description="Date d'embauche (format: YYYY-MM-DD)")
    departement: Optional[str] = Field(None, max_length=100, description="Département (max 100 caractères)")
    
    @field_validator('nom', 'prenom', 'poste')
    @classmethod
    def validate_non_empty(cls, v: Optional[str]) -> Optional[str]:
        """Valide que les champs ne sont pas vides ou ne contiennent que des espaces"""
        if v is not None:
            if not v.strip():
                raise ValueError("Ce champ ne peut pas être vide")
            return v.strip()
        return v
    
    @field_validator('salaire')
    @classmethod
    def validate_salaire_positif(cls, v: Optional[float]) -> Optional[float]:
        """Valide que le salaire est positif"""
        if v is not None and v <= 0:
            raise ValueError("Le salaire doit être un nombre positif")
        return v
    
    @field_validator('date_embauche')
    @classmethod
    def validate_date_embauche(cls, v: Optional[date]) -> Optional[date]:
        """Valide que la date d'embauche n'est pas dans le futur"""
        if v is not None:
            today = date.today()
            if v > today:
                raise ValueError("La date d'embauche ne peut pas être dans le futur")
        return v

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


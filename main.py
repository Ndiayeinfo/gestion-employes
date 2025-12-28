from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="API de Gestion des Employés",
    description="API CRUD pour gérer les employés d'une entreprise",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route racine
@app.get("/")
def read_root():
    return {
        "message": "API de Gestion des Employés",
        "documentation": "/docs",
        "endpoints": {
            "GET /employes": "Liste tous les employés",
            "GET /employes/{id}": "Récupère un employé par ID",
            "POST /employes": "Crée un nouvel employé",
            "PUT /employes/{id}": "Met à jour un employé",
            "DELETE /employes/{id}": "Supprime un employé"
        }
    }

# GET - Liste tous les employés
@app.get("/employes", response_model=List[schemas.EmployeResponse])
def lire_employes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste de tous les employés avec pagination.
    """
    employes = db.query(models.Employe).offset(skip).limit(limit).all()
    return employes

# GET - Récupère un employé par ID
@app.get("/employes/{employe_id}", response_model=schemas.EmployeResponse)
def lire_employe(employe_id: int, db: Session = Depends(get_db)):
    """
    Récupère un employé spécifique par son ID.
    """
    employe = db.query(models.Employe).filter(models.Employe.id == employe_id).first()
    if not employe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employé avec l'ID {employe_id} non trouvé"
        )
    return employe

# POST - Crée un nouvel employé
@app.post("/employes", response_model=schemas.EmployeResponse, status_code=status.HTTP_201_CREATED)
def creer_employe(employe: schemas.EmployeCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel employé.
    """
    # Vérifier si l'email existe déjà
    db_employe = db.query(models.Employe).filter(models.Employe.email == employe.email).first()
    if db_employe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un employé avec cet email existe déjà"
        )
    
    # Créer le nouvel employé
    nouvel_employe = models.Employe(**employe.dict())
    db.add(nouvel_employe)
    db.commit()
    db.refresh(nouvel_employe)
    return nouvel_employe

# PUT - Met à jour un employé
@app.put("/employes/{employe_id}", response_model=schemas.EmployeResponse)
def mettre_a_jour_employe(
    employe_id: int, 
    employe_update: schemas.EmployeUpdate, 
    db: Session = Depends(get_db)
):
    """
    Met à jour les informations d'un employé existant.
    """
    employe = db.query(models.Employe).filter(models.Employe.id == employe_id).first()
    if not employe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employé avec l'ID {employe_id} non trouvé"
        )
    
    # Vérifier si l'email est modifié et s'il existe déjà
    if employe_update.email and employe_update.email != employe.email:
        db_employe_existant = db.query(models.Employe).filter(
            models.Employe.email == employe_update.email
        ).first()
        if db_employe_existant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un employé avec cet email existe déjà"
            )
    
    # Mettre à jour uniquement les champs fournis
    update_data = employe_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employe, field, value)
    
    db.commit()
    db.refresh(employe)
    return employe

# DELETE - Supprime un employé
@app.delete("/employes/{employe_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_employe(employe_id: int, db: Session = Depends(get_db)):
    """
    Supprime un employé de la base de données.
    """
    employe = db.query(models.Employe).filter(models.Employe.id == employe_id).first()
    if not employe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employé avec l'ID {employe_id} non trouvé"
        )
    
    db.delete(employe)
    db.commit()
    return None

# GET - Recherche d'employés par nom ou email
@app.get("/employes/recherche/{terme}", response_model=List[schemas.EmployeResponse])
def rechercher_employes(terme: str, db: Session = Depends(get_db)):
    """
    Recherche des employés par nom, prénom ou email.
    """
    employes = db.query(models.Employe).filter(
        (models.Employe.nom.contains(terme)) |
        (models.Employe.prenom.contains(terme)) |
        (models.Employe.email.contains(terme))
    ).all()
    return employes


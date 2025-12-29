from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import models
import schemas
from database import engine, get_db

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI(
    title="API de Gestion des Employés",
    description="API CRUD pour gérer les employés d'une entreprise",
    version="1.1.0"
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
        "version": "1.1.0",
        "documentation": "/docs",
        "endpoints": {
            "GET /employes": "Liste tous les employés (avec filtres avancés)",
            "GET /employes/{id}": "Récupère un employé par ID",
            "POST /employes": "Crée un nouvel employé",
            "PUT /employes/{id}": "Met à jour un employé",
            "DELETE /employes/{id}": "Supprime un employé",
            "GET /employes/recherche/{terme}": "Recherche d'employés",
            "GET /employes/statistiques": "Statistiques des employés"
        },
        "filtres_disponibles": {
            "departement": "Filtrer par département",
            "salaire_min": "Salaire minimum",
            "salaire_max": "Salaire maximum",
            "date_embauche_apres": "Date d'embauche après (YYYY-MM-DD)",
            "date_embauche_avant": "Date d'embauche avant (YYYY-MM-DD)",
            "poste": "Filtrer par poste (recherche partielle)"
        }
    }

# GET - Liste tous les employés
@app.get("/employes", response_model=List[schemas.EmployeResponse])
def lire_employes(
    skip: int = 0, 
    limit: int = 100,
    departement: Optional[str] = None,
    salaire_min: Optional[float] = None,
    salaire_max: Optional[float] = None,
    date_embauche_apres: Optional[date] = None,
    date_embauche_avant: Optional[date] = None,
    poste: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les employés avec pagination et filtres avancés.
    
    Filtres disponibles :
    - departement : Filtrer par département
    - salaire_min : Salaire minimum
    - salaire_max : Salaire maximum
    - date_embauche_apres : Date d'embauche après cette date (format: YYYY-MM-DD)
    - date_embauche_avant : Date d'embauche avant cette date (format: YYYY-MM-DD)
    - poste : Filtrer par poste
    """
    query = db.query(models.Employe)
    
    # Appliquer les filtres
    if departement:
        query = query.filter(models.Employe.departement == departement)
    
    if salaire_min is not None:
        query = query.filter(models.Employe.salaire >= salaire_min)
    
    if salaire_max is not None:
        query = query.filter(models.Employe.salaire <= salaire_max)
    
    if date_embauche_apres:
        query = query.filter(models.Employe.date_embauche >= date_embauche_apres)
    
    if date_embauche_avant:
        query = query.filter(models.Employe.date_embauche <= date_embauche_avant)
    
    if poste:
        query = query.filter(models.Employe.poste.contains(poste))
    
    # Appliquer la pagination
    employes = query.offset(skip).limit(limit).all()
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

# GET - Statistiques des employés
@app.get("/employes/statistiques")
def obtenir_statistiques(db: Session = Depends(get_db)):
    """
    Retourne des statistiques sur les employés.
    """
    from sqlalchemy import func
    
    total = db.query(func.count(models.Employe.id)).scalar()
    
    # Nombre par département
    par_departement = db.query(
        models.Employe.departement,
        func.count(models.Employe.id).label('nombre')
    ).group_by(models.Employe.departement).all()
    
    # Salaire moyen
    salaire_moyen = db.query(func.avg(models.Employe.salaire)).scalar()
    
    # Salaire minimum et maximum
    salaire_min = db.query(func.min(models.Employe.salaire)).scalar()
    salaire_max = db.query(func.max(models.Employe.salaire)).scalar()
    
    # Nombre par poste
    par_poste = db.query(
        models.Employe.poste,
        func.count(models.Employe.id).label('nombre')
    ).group_by(models.Employe.poste).all()
    
    return {
        "total_employes": total,
        "salaire_moyen": round(salaire_moyen, 2) if salaire_moyen else None,
        "salaire_minimum": salaire_min,
        "salaire_maximum": salaire_max,
        "par_departement": {dept: count for dept, count in par_departement if dept},
        "par_poste": {poste: count for poste, count in par_poste}
    }


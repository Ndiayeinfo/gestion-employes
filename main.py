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
    version="1.2.0"
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
        },
        "pagination": {
            "ancienne_methode": "skip et limit (rétrocompatible)",
            "nouvelle_methode": "page (commence à 1) et per_page (défaut: 20)"
        },
        "tri": {
            "colonnes": "nom, prenom, email, salaire, date_embauche, departement, poste",
            "ordre": "asc (défaut) ou desc"
        }
    }

# GET - Liste tous les employés
@app.get("/employes", response_model=List[schemas.EmployeResponse])
def lire_employes(
    # Pagination (ancienne méthode - rétrocompatible)
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    # Pagination améliorée (nouvelle méthode)
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    # Filtres
    departement: Optional[str] = None,
    salaire_min: Optional[float] = None,
    salaire_max: Optional[float] = None,
    date_embauche_apres: Optional[date] = None,
    date_embauche_avant: Optional[date] = None,
    poste: Optional[str] = None,
    # Tri
    sort: Optional[str] = None,  # nom, prenom, email, salaire, date_embauche, departement, poste
    order: Optional[str] = "asc",  # asc ou desc
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les employés avec pagination améliorée, filtres avancés et tri.
    
    **Pagination** :
    - Ancienne méthode (rétrocompatible) : `skip` et `limit`
    - Nouvelle méthode : `page` (commence à 1) et `per_page` (défaut: 20)
    
    **Filtres disponibles** :
    - departement : Filtrer par département
    - salaire_min : Salaire minimum
    - salaire_max : Salaire maximum
    - date_embauche_apres : Date d'embauche après cette date (format: YYYY-MM-DD)
    - date_embauche_avant : Date d'embauche avant cette date (format: YYYY-MM-DD)
    - poste : Filtrer par poste (recherche partielle)
    
    **Tri** :
    - sort : Colonne à trier (nom, prenom, email, salaire, date_embauche, departement, poste)
    - order : Ordre de tri (asc ou desc, défaut: asc)
    """
    from sqlalchemy import asc, desc
    
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
    
    # Appliquer le tri
    if sort:
        sort_column = None
        sort_lower = sort.lower()
        
        if sort_lower == "nom":
            sort_column = models.Employe.nom
        elif sort_lower == "prenom":
            sort_column = models.Employe.prenom
        elif sort_lower == "email":
            sort_column = models.Employe.email
        elif sort_lower == "salaire":
            sort_column = models.Employe.salaire
        elif sort_lower == "date_embauche":
            sort_column = models.Employe.date_embauche
        elif sort_lower == "departement":
            sort_column = models.Employe.departement
        elif sort_lower == "poste":
            sort_column = models.Employe.poste
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Colonne de tri invalide: {sort}. Colonnes valides: nom, prenom, email, salaire, date_embauche, departement, poste"
            )
        
        if sort_column:
            if order and order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
    else:
        # Tri par défaut : par ID (ordre d'insertion)
        query = query.order_by(asc(models.Employe.id))
    
    # Gérer la pagination (nouvelle méthode prioritaire)
    if page is not None and per_page is not None:
        # Nouvelle méthode : page/per_page
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le numéro de page doit être supérieur ou égal à 1"
            )
        if per_page < 1 or per_page > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="per_page doit être entre 1 et 100"
            )
        offset = (page - 1) * per_page
        limit_value = per_page
    elif skip is not None and limit is not None:
        # Ancienne méthode : skip/limit (rétrocompatible)
        offset = skip
        limit_value = min(limit, 100)  # Limiter à 100 pour éviter les abus
    else:
        # Défaut : première page, 20 éléments
        offset = 0
        limit_value = 20
    
    # Appliquer la pagination
    employes = query.offset(offset).limit(limit_value).all()
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
    
    Les données sont automatiquement validées :
    - Nom, prénom et poste : obligatoires, 1-100 caractères
    - Email : obligatoire, format valide, unique
    - Salaire : optionnel, doit être positif si fourni
    - Date d'embauche : optionnel, ne peut pas être dans le futur
    """
    # Vérifier si l'email existe déjà
    db_employe = db.query(models.Employe).filter(models.Employe.email == employe.email).first()
    if db_employe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Email déjà utilisé",
                "message": f"Un employé avec l'email '{employe.email}' existe déjà",
                "email": employe.email
            }
        )
    
    try:
        # Créer le nouvel employé
        nouvel_employe = models.Employe(**employe.model_dump())
        db.add(nouvel_employe)
        db.commit()
        db.refresh(nouvel_employe)
        return nouvel_employe
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Erreur lors de la création",
                "message": "Une erreur est survenue lors de la création de l'employé"
            }
        )

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
                detail=f"Un employé avec l'email '{employe_update.email}' existe déjà. L'email doit être unique."
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


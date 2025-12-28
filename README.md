# API de Gestion des Employés

Application CRUD (Create, Read, Update, Delete) pour gérer les employés d'une entreprise, construite avec FastAPI.

## Fonctionnalités

- ✅ Créer un nouvel employé
- ✅ Lire la liste de tous les employés
- ✅ Lire les détails d'un employé spécifique
- ✅ Mettre à jour les informations d'un employé
- ✅ Supprimer un employé
- ✅ Rechercher des employés par nom, prénom ou email
- ✅ Documentation interactive automatique (Swagger UI)

## Prérequis

### Pour l'exécution locale
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Pour Docker
- Docker (version 20.10 ou supérieure)
- Docker Compose (optionnel, mais recommandé)

## Installation

1. **Créer un environnement virtuel (recommandé)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## Lancement de l'application

### Option 1 : Exécution locale (sans Docker)

```bash
uvicorn main:app --reload
```

L'application sera accessible à l'adresse : **http://localhost:8000**

### Option 2 : Avec Docker

#### Méthode 1 : Docker Compose (recommandé)

```bash
# Construire et lancer le conteneur
docker-compose up --build

# Ou en arrière-plan
docker-compose up -d --build

# Arrêter le conteneur
docker-compose down
```

#### Méthode 2 : Docker uniquement

```bash
# Construire l'image
docker build -t gestion-employes:latest .

# Lancer le conteneur
docker run -d -p 8000:8000 --name gestion_employes_api gestion-employes:latest

# Voir les logs
docker logs -f gestion_employes_api

# Arrêter le conteneur
docker stop gestion_employes_api

# Supprimer le conteneur
docker rm gestion_employes_api
```

#### Persistance des données avec Docker

Avec Docker Compose, les données sont automatiquement persistées dans le dossier `./data` grâce au volume monté. Si vous utilisez Docker seul, vous pouvez monter un volume :

```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e SQLALCHEMY_DATABASE_URL=sqlite:///./data/employes.db \
  --name gestion_employes_api \
  gestion-employes:latest
```

L'application sera accessible à l'adresse : **http://localhost:8000**

## Documentation interactive

Une fois l'application lancée, vous pouvez accéder à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Endpoints disponibles

### 1. Liste tous les employés
```
GET /employes
```
Paramètres optionnels :
- `skip` : nombre d'employés à sauter (par défaut: 0)
- `limit` : nombre maximum d'employés à retourner (par défaut: 100)

### 2. Récupère un employé par ID
```
GET /employes/{employe_id}
```

### 3. Crée un nouvel employé
```
POST /employes
```
Corps de la requête (JSON) :
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "telephone": "+33123456789",
  "poste": "Développeur",
  "salaire": 50000.0,
  "date_embauche": "2023-01-15",
  "departement": "IT"
}
```

### 4. Met à jour un employé
```
PUT /employes/{employe_id}
```
Corps de la requête (JSON) - tous les champs sont optionnels :
```json
{
  "salaire": 55000.0,
  "poste": "Développeur Senior"
}
```

### 5. Supprime un employé
```
DELETE /employes/{employe_id}
```

### 6. Recherche d'employés
```
GET /employes/recherche/{terme}
```
Recherche dans le nom, prénom ou email.

## Exemples d'utilisation avec curl

### Créer un employé
```bash
curl -X POST "http://localhost:8000/employes" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Martin",
    "prenom": "Sophie",
    "email": "sophie.martin@example.com",
    "poste": "Chef de projet",
    "salaire": 60000.0
  }'
```

### Lister tous les employés
```bash
curl "http://localhost:8000/employes"
```

### Récupérer un employé par ID
```bash
curl "http://localhost:8000/employes/1"
```

### Mettre à jour un employé
```bash
curl -X PUT "http://localhost:8000/employes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "salaire": 65000.0
  }'
```

### Supprimer un employé
```bash
curl -X DELETE "http://localhost:8000/employes/1"
```

### Rechercher des employés
```bash
curl "http://localhost:8000/employes/recherche/dupont"
```

## Structure du projet

```
gestion_employes/
├── main.py              # Application FastAPI principale avec les routes
├── models.py            # Modèles SQLAlchemy (structure de la base de données)
├── schemas.py           # Schémas Pydantic (validation des données)
├── database.py          # Configuration de la base de données
├── requirements.txt     # Dépendances Python
├── Dockerfile           # Configuration Docker
├── docker-compose.yml   # Configuration Docker Compose
├── .dockerignore        # Fichiers ignorés par Docker
├── README.md            # Ce fichier
└── employes.db          # Base de données SQLite (créée automatiquement)
```

## Base de données

L'application utilise SQLite par défaut. Le fichier `employes.db` sera créé automatiquement au premier lancement.

### Structure de la table `employes`

- `id` : Identifiant unique (entier, clé primaire)
- `nom` : Nom de l'employé (texte, requis)
- `prenom` : Prénom de l'employé (texte, requis)
- `email` : Email de l'employé (texte, unique, requis)
- `telephone` : Numéro de téléphone (texte, optionnel)
- `poste` : Poste occupé (texte, requis)
- `salaire` : Salaire (décimal, optionnel)
- `date_embauche` : Date d'embauche (date, optionnel)
- `departement` : Département (texte, optionnel)

## Notes

- L'email doit être unique pour chaque employé
- La validation des emails est automatique grâce à Pydantic
- Les dates doivent être au format ISO (YYYY-MM-DD)
- Le mode `--reload` permet le rechargement automatique lors des modifications du code

## Prochaines améliorations possibles

- Authentification et autorisation
- Pagination améliorée
- Filtres avancés (par département, salaire, etc.)
- Export des données (CSV, Excel)
- Tests unitaires et d'intégration
- Migration vers PostgreSQL pour la production


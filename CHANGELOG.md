# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.3.0] - 2024-12-28

### Ajouté
- Validations de données améliorées :
  - Validation des champs obligatoires (nom, prénom, poste) avec suppression automatique des espaces
  - Validation du salaire (doit être un nombre positif)
  - Validation de la date d'embauche (ne peut pas être dans le futur)
  - Limites de longueur pour tous les champs texte (nom, prénom, poste: 1-100 caractères, téléphone: max 20, département: max 100)
- Messages d'erreur améliorés et plus descriptifs
- Documentation des champs avec descriptions Pydantic

### Modifié
- Version de l'API mise à jour à 1.3.0
- Messages d'erreur HTTP plus clairs et informatifs

## [1.2.0] - 2024-12-28

### Ajouté
- Tri par colonnes sur l'endpoint GET /employes :
  - Tri par nom, prénom, email, salaire, date d'embauche, département, poste
  - Ordre ascendant (asc) ou descendant (desc)
- Pagination améliorée :
  - Nouvelle méthode avec `page` (commence à 1) et `per_page` (défaut: 20)
  - Rétrocompatible avec l'ancienne méthode `skip` et `limit`
  - Validation des paramètres (page >= 1, per_page entre 1 et 100)

### Modifié
- Version de l'API mise à jour à 1.2.0
- Documentation améliorée avec les options de tri et pagination

## [1.1.0] - 2024-12-28

### Ajouté
- Filtres avancés sur l'endpoint GET /employes :
  - Filtre par département
  - Filtre par fourchette de salaire (salaire_min, salaire_max)
  - Filtre par date d'embauche (date_embauche_apres, date_embauche_avant)
  - Filtre par poste (recherche partielle)
- Nouvel endpoint GET /employes/statistiques pour obtenir des statistiques :
  - Nombre total d'employés
  - Salaire moyen, minimum et maximum
  - Répartition par département
  - Répartition par poste
- ROADMAP.md pour planifier les futures améliorations

### Modifié
- Version de l'API mise à jour à 1.1.0
- Documentation de l'endpoint GET /employes améliorée avec les nouveaux filtres

## [1.0.0] - 2024-12-28

### Ajouté
- API CRUD complète pour la gestion des employés
- Endpoints :
  - GET /employes - Liste tous les employés avec pagination
  - GET /employes/{id} - Récupère un employé par ID
  - POST /employes - Crée un nouvel employé
  - PUT /employes/{id} - Met à jour un employé
  - DELETE /employes/{id} - Supprime un employé
  - GET /employes/recherche/{terme} - Recherche d'employés
- Modèle de données avec les champs : nom, prénom, email, téléphone, poste, salaire, date d'embauche, département
- Validation des emails avec Pydantic
- Documentation interactive (Swagger UI et ReDoc)
- Support Docker et Docker Compose
- Scripts de déploiement pour Google Compute Engine
- Stratégie de branches documentée


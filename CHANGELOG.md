# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.1.0] - En développement

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


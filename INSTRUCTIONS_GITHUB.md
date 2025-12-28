# Instructions pour créer le dépôt GitHub et pousser le code

## Étape 1 : Créer le dépôt sur GitHub

1. Allez sur : **https://github.com/new**
2. Remplissez les informations :
   - **Repository name** : `gestion-employes`
   - **Description** : `API CRUD de gestion des employés avec FastAPI, Docker et Docker Compose`
   - **Visibilité** : Choisissez Public ou Private selon vos préférences
   - **IMPORTANT** : NE cochez PAS "Add a README file", "Add .gitignore", ou "Choose a license" (nous avons déjà ces fichiers)
3. Cliquez sur **"Create repository"**

## Étape 2 : Pousser le code

Une fois le dépôt créé, exécutez cette commande dans le terminal (vous êtes déjà dans le bon dossier) :

```bash
git push -u origin main
```

Si vous êtes invité à vous authentifier :
- Utilisez votre nom d'utilisateur GitHub : `Ndiayeinfo`
- Pour le mot de passe, utilisez un **Personal Access Token** (pas votre mot de passe GitHub)
  - Créez un token sur : https://github.com/settings/tokens
  - Sélectionnez les permissions : `repo` (accès complet aux dépôts)

## Vérification

Après le push, votre code sera disponible sur :
**https://github.com/Ndiayeinfo/gestion-employes**

## Commandes Git utiles pour la suite

Selon votre stratégie de branches :

```bash
# Créer une branche feature
git checkout -b feature:nom-fonctionnalite

# Créer une branche fixing
git checkout -b fixing:nom-bug

# Pousser une branche
git push -u origin feature:nom-fonctionnalite

# Revenir sur main
git checkout main
```


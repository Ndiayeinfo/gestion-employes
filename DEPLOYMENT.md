# Guide de déploiement sur Google Compute Engine

Ce guide explique comment déployer l'API de gestion des employés sur une machine virtuelle Google Compute Engine en suivant la stratégie de branches définie.

## Prérequis

- Compte Google Cloud Platform (GCP) avec un projet actif
- Google Cloud SDK (`gcloud`) installé et configuré
- Accès en écriture au dépôt GitHub
- Docker et Docker Compose installés localement (pour tester)

## Stratégie de déploiement

Selon notre stratégie de branches, nous suivons ce processus :

1. **Créer une branche de release** : `release-X.Y` (ex: `release-1.0`)
2. **Stabiliser la version** : tests, corrections de bugs si nécessaire
3. **Créer un tag** : `vX.Y.Z` (ex: `v1.0.0`) quand la version est prête
4. **Déployer le tag** : utiliser le tag (pas la branche) pour déployer sur GCE

## Étape 1 : Préparer la release

### 1.1 Créer la branche de release

```bash
git checkout main
git pull origin main
git checkout -b release-1.0
```

### 1.2 Vérifier que tout est prêt

- Tous les tests passent
- La documentation est à jour
- Le code est stable

### 1.3 Créer le tag de version

```bash
# Sur la branche release-1.0
git tag v1.0.0
git push origin release-1.0
git push origin v1.0.0  # Pousser le tag vers GitHub
```

## Étape 2 : Créer l'instance Compute Engine

### Option A : Script automatique (Linux/Mac)

```bash
chmod +x create-gce-instance.sh
./create-gce-instance.sh gestion-employes-vm us-central1-a
```

### Option B : Script PowerShell (Windows)

```powershell
.\create-gce-instance.ps1 -InstanceName "gestion-employes-vm" -Zone "us-central1-a"
```

### Option C : Commande gcloud manuelle

```bash
gcloud compute instances create gestion-employes-vm \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server
```

**Note** : Le script automatique installe Docker, Docker Compose et Git sur l'instance. Si vous créez l'instance manuellement, installez ces outils vous-même.

## Étape 3 : Configurer le firewall

Autoriser le trafic HTTP sur le port 8000 :

```bash
gcloud compute firewall-rules create allow-http-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP traffic on port 8000"
```

## Étape 4 : Déployer l'application

### Option A : Script automatique (Linux/Mac)

```bash
chmod +x deploy-gce.sh
./deploy-gce.sh v1.0.0 gestion-employes-vm us-central1-a
```

### Option B : Script PowerShell (Windows)

```powershell
.\deploy-gce.ps1 -Tag "v1.0.0" -InstanceName "gestion-employes-vm" -Zone "us-central1-a"
```

### Option C : Déploiement manuel

```bash
# Se connecter à l'instance
gcloud compute ssh gestion-employes-vm --zone=us-central1-a

# Sur l'instance
cd /opt
sudo mkdir -p gestion-employes
sudo chown $USER:$USER gestion-employes
cd gestion-employes

# Cloner le dépôt et checkout le tag
git clone https://github.com/Ndiayeinfo/gestion-employes.git .
git checkout tags/v1.0.0

# Lancer avec Docker Compose
docker-compose up -d --build
```

## Étape 5 : Vérifier le déploiement

### Obtenir l'adresse IP de l'instance

```bash
gcloud compute instances describe gestion-employes-vm \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

### Tester l'API

```bash
# Remplacer <IP> par l'adresse IP obtenue
curl http://<IP>:8000/
curl http://<IP>:8000/docs
```

## Gestion des versions et mises à jour

### Déployer une nouvelle version

1. Créer une nouvelle branche de release : `release-1.1`
2. Faire les modifications nécessaires
3. Créer un nouveau tag : `v1.1.0`
4. Déployer avec le script : `./deploy-gce.sh v1.1.0 gestion-employes-vm us-central1-a`

### Corriger un bug en production

1. Créer une branche `fixing:nom-bug` à partir de `release-1.0`
2. Corriger le bug
3. Fusionner dans `release-1.0`
4. Créer un nouveau tag : `v1.0.1`
5. Déployer : `./deploy-gce.sh v1.0.1 gestion-employes-vm us-central1-a`

## Commandes utiles

### Voir les logs de l'application

```bash
gcloud compute ssh gestion-employes-vm --zone=us-central1-a \
    --command="cd /opt/gestion-employes && docker-compose logs -f"
```

### Redémarrer l'application

```bash
gcloud compute ssh gestion-employes-vm --zone=us-central1-a \
    --command="cd /opt/gestion-employes && docker-compose restart"
```

### Arrêter l'application

```bash
gcloud compute ssh gestion-employes-vm --zone=us-central1-a \
    --command="cd /opt/gestion-employes && docker-compose down"
```

### Mettre à jour vers une nouvelle version

```bash
# Le script de déploiement gère automatiquement la mise à jour
./deploy-gce.sh v1.0.1 gestion-employes-vm us-central1-a
```

## Sécurité

- **Firewall** : Limitez l'accès au port 8000 à des IPs spécifiques si nécessaire
- **HTTPS** : Configurez un reverse proxy (nginx) avec Let's Encrypt pour HTTPS
- **Authentification** : Ajoutez une authentification à l'API si nécessaire
- **Secrets** : Utilisez Google Secret Manager pour les secrets de production

## Coûts estimés

- Instance e2-medium : ~$25-30/mois
- Stockage (20GB) : ~$2-3/mois
- Trafic réseau : variable selon l'utilisation

## Support

En cas de problème :
1. Vérifiez les logs : `docker-compose logs`
2. Vérifiez l'état de l'instance : `gcloud compute instances describe gestion-employes-vm --zone=us-central1-a`
3. Vérifiez les règles de firewall : `gcloud compute firewall-rules list`


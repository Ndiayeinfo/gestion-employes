#!/bin/bash
# Script pour créer une instance Compute Engine pour l'application
# Usage: ./create-gce-instance.sh <instance-name> <zone> [project-id]
# Exemple: ./create-gce-instance.sh gestion-employes-vm us-central1-a

set -e

INSTANCE_NAME=$1
ZONE=$2
PROJECT_ID=${3:-$(gcloud config get-value project 2>/dev/null || echo "")}

if [ -z "$INSTANCE_NAME" ] || [ -z "$ZONE" ]; then
    echo "❌ Erreur: Paramètres manquants"
    echo "Usage: ./create-gce-instance.sh <instance-name> <zone> [project-id]"
    echo "Exemple: ./create-gce-instance.sh gestion-employes-vm us-central1-a"
    exit 1
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Erreur: PROJECT_ID non défini. Spécifiez-le ou configurez gcloud: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "🔧 Création de l'instance Compute Engine: $INSTANCE_NAME"
echo "📍 Zone: $ZONE"
echo "📦 Projet: $PROJECT_ID"
echo ""

# Vérifier si l'instance existe déjà
if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID &>/dev/null; then
    echo "⚠️  L'instance $INSTANCE_NAME existe déjà dans la zone $ZONE"
    read -p "Voulez-vous continuer quand même? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Créer l'instance
echo "🚀 Création de l'instance..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --project=$PROJECT_ID \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
# Installation de Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Installation de Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Installation de Git
sudo apt-get update
sudo apt-get install -y git curl

# Création du répertoire de l'application
sudo mkdir -p /opt/gestion-employes
sudo chown $USER:$USER /opt/gestion-employes

echo "✅ Installation terminée"
'

# Attendre que l'instance soit prête
echo "⏳ Attente que l'instance soit prête..."
sleep 30

# Configurer le firewall pour autoriser le trafic HTTP
echo "🔥 Configuration du firewall..."
gcloud compute firewall-rules create allow-http-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP traffic on port 8000" \
    --project=$PROJECT_ID \
    2>/dev/null || echo "⚠️  La règle de firewall existe peut-être déjà"

# Obtenir l'adresse IP
IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo ""
echo "✅ Instance créée avec succès!"
echo "🌐 Adresse IP: $IP"
echo "📋 Prochaines étapes:"
echo "  1. Attendez 2-3 minutes que l'installation soit terminée"
echo "  2. Déployez l'application avec: ./deploy-gce.sh v1.0.0 $INSTANCE_NAME $ZONE"
echo ""
echo "💡 Pour vérifier que l'instance est prête:"
echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='docker --version && docker-compose --version'"


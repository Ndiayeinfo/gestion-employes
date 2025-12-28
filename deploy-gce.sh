#!/bin/bash
# Script de déploiement sur Google Compute Engine
# Usage: ./deploy-gce.sh <tag> <instance-name> <zone>
# Exemple: ./deploy-gce.sh v1.0.0 my-app-instance us-central1-a

set -e

TAG=$1
INSTANCE_NAME=$2
ZONE=$3
PROJECT_ID=${4:-$(gcloud config get-value project 2>/dev/null || echo "")}

if [ -z "$TAG" ] || [ -z "$INSTANCE_NAME" ] || [ -z "$ZONE" ]; then
    echo "❌ Erreur: Paramètres manquants"
    echo "Usage: ./deploy-gce.sh <tag> <instance-name> <zone> [project-id]"
    echo "Exemple: ./deploy-gce.sh v1.0.0 gestion-employes-vm us-central1-a"
    exit 1
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Erreur: PROJECT_ID non défini. Spécifiez-le ou configurez gcloud: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "🚀 Déploiement de la version $TAG sur $INSTANCE_NAME (zone: $ZONE)"
echo "📦 Projet GCP: $PROJECT_ID"
echo ""

# Vérifier que l'instance existe
echo "🔍 Vérification de l'instance..."
if ! gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID &>/dev/null; then
    echo "❌ L'instance $INSTANCE_NAME n'existe pas dans la zone $ZONE"
    echo "💡 Créez l'instance d'abord avec: ./create-gce-instance.sh"
    exit 1
fi

# Vérifier que le tag existe localement
if ! git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "❌ Le tag $TAG n'existe pas localement"
    echo "💡 Créez le tag d'abord avec: git tag $TAG"
    exit 1
fi

echo "✅ Tag $TAG trouvé localement"
echo ""

# Déployer sur l'instance
echo "📥 Déploiement du code sur l'instance..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --project=$PROJECT_ID << DEPLOY_SCRIPT
  set -e
  cd /opt/gestion-employes || { echo "Création du répertoire..."; sudo mkdir -p /opt/gestion-employes; cd /opt/gestion-employes; }
  
  echo "📥 Récupération du tag $TAG depuis GitHub..."
  if [ -d .git ]; then
    git fetch --all --tags
    git checkout tags/$TAG
  else
    git clone https://github.com/Ndiayeinfo/gestion-employes.git .
    git checkout tags/$TAG
  fi
  
  echo "🐳 Arrêt des conteneurs existants..."
  docker-compose down || true
  
  echo "🐳 Construction et démarrage des nouveaux conteneurs..."
  docker-compose up -d --build
  
  echo "⏳ Attente du démarrage de l'application..."
  sleep 10
  
  echo "🔍 Vérification de l'état de l'application..."
  if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Application démarrée avec succès!"
    echo "📊 Version déployée: \$(git describe --tags)"
  else
    echo "⚠️  L'application ne répond pas encore. Vérifiez les logs avec: docker-compose logs"
  fi
DEPLOY_SCRIPT

echo ""
echo "✅ Déploiement terminé!"
echo "🌐 Votre application devrait être accessible sur: http://\$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='cd /opt/gestion-employes && docker-compose logs -f'"
echo "  - Redémarrer: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='cd /opt/gestion-employes && docker-compose restart'"
echo "  - Arrêter: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='cd /opt/gestion-employes && docker-compose down'"


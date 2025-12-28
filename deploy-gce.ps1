# Script de déploiement sur Google Compute Engine (PowerShell)
# Usage: .\deploy-gce.ps1 -Tag v1.0.0 -InstanceName "gestion-employes-vm" -Zone "us-central1-a"

param(
    [Parameter(Mandatory=$true)]
    [string]$Tag,
    
    [Parameter(Mandatory=$true)]
    [string]$InstanceName,
    
    [Parameter(Mandatory=$true)]
    [string]$Zone,
    
    [string]$ProjectId = ""
)

if ([string]::IsNullOrEmpty($ProjectId)) {
    $ProjectId = gcloud config get-value project 2>$null
    if ([string]::IsNullOrEmpty($ProjectId)) {
        Write-Host "❌ Erreur: PROJECT_ID non défini. Spécifiez-le avec -ProjectId ou configurez gcloud" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🚀 Déploiement de la version $Tag sur $InstanceName (zone: $Zone)" -ForegroundColor Green
Write-Host "📦 Projet GCP: $ProjectId" -ForegroundColor Cyan
Write-Host ""

# Vérifier que l'instance existe
Write-Host "🔍 Vérification de l'instance..." -ForegroundColor Yellow
$instanceExists = gcloud compute instances describe $InstanceName --zone=$Zone --project=$ProjectId 2>$null
if (-not $instanceExists) {
    Write-Host "❌ L'instance $InstanceName n'existe pas dans la zone $Zone" -ForegroundColor Red
    Write-Host "💡 Créez l'instance d'abord avec: .\create-gce-instance.ps1" -ForegroundColor Yellow
    exit 1
}

# Vérifier que le tag existe localement
$tagExists = git rev-parse "$Tag" 2>$null
if (-not $tagExists) {
    Write-Host "❌ Le tag $Tag n'existe pas localement" -ForegroundColor Red
    Write-Host "💡 Créez le tag d'abord avec: git tag $Tag" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Tag $Tag trouvé localement" -ForegroundColor Green
Write-Host ""

# Déployer sur l'instance
Write-Host "📥 Déploiement du code sur l'instance..." -ForegroundColor Yellow

$deployScript = @"
set -e
cd /opt/gestion-employes || { echo "Création du répertoire..."; sudo mkdir -p /opt/gestion-employes; cd /opt/gestion-employes; }

echo "📥 Récupération du tag $Tag depuis GitHub..."
if [ -d .git ]; then
  git fetch --all --tags
  git checkout tags/$Tag
else
  git clone https://github.com/Ndiayeinfo/gestion-employes.git .
  git checkout tags/$Tag
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
"@

gcloud compute ssh $InstanceName --zone=$Zone --project=$ProjectId --command=$deployScript

$ip = gcloud compute instances describe $InstanceName --zone=$Zone --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

Write-Host ""
Write-Host "✅ Déploiement terminé!" -ForegroundColor Green
Write-Host "🌐 Votre application devrait être accessible sur: http://$ip:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Commandes utiles:" -ForegroundColor Yellow
Write-Host "  - Voir les logs: gcloud compute ssh $InstanceName --zone=$Zone --command='cd /opt/gestion-employes && docker-compose logs -f'"
Write-Host "  - Redémarrer: gcloud compute ssh $InstanceName --zone=$Zone --command='cd /opt/gestion-employes && docker-compose restart'"
Write-Host "  - Arrêter: gcloud compute ssh $InstanceName --zone=$Zone --command='cd /opt/gestion-employes && docker-compose down'"


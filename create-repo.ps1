# Script pour créer le dépôt GitHub et pousser le code
# Remplacez YOUR_GITHUB_TOKEN par votre token d'accès personnel GitHub

$repoName = "gestion-employes"
$username = "Ndiayeinfo"
$description = "API CRUD de gestion des employés avec FastAPI, Docker et Docker Compose"

Write-Host "Création du dépôt GitHub: $repoName" -ForegroundColor Green

# Si vous avez un token GitHub, décommentez et utilisez cette section:
# $token = "YOUR_GITHUB_TOKEN"
# $headers = @{
#     "Authorization" = "token $token"
#     "Accept" = "application/vnd.github.v3+json"
# }
# $body = @{
#     name = $repoName
#     description = $description
#     private = $false
# } | ConvertTo-Json
# 
# try {
#     $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body
#     Write-Host "Dépôt créé avec succès: $($response.html_url)" -ForegroundColor Green
# } catch {
#     Write-Host "Erreur lors de la création du dépôt: $_" -ForegroundColor Red
#     Write-Host "Veuillez créer le dépôt manuellement sur https://github.com/new" -ForegroundColor Yellow
# }

Write-Host "`nInstructions manuelles:" -ForegroundColor Yellow
Write-Host "1. Allez sur https://github.com/new" -ForegroundColor Cyan
Write-Host "2. Nom du dépôt: $repoName" -ForegroundColor Cyan
Write-Host "3. Description: $description" -ForegroundColor Cyan
Write-Host "4. Choisissez Public ou Private" -ForegroundColor Cyan
Write-Host "5. NE cochez PAS 'Initialize this repository with a README'" -ForegroundColor Cyan
Write-Host "6. Cliquez sur 'Create repository'" -ForegroundColor Cyan
Write-Host "`nEnsuite, exécutez ces commandes:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/$username/$repoName.git" -ForegroundColor Green
Write-Host "git push -u origin main" -ForegroundColor Green


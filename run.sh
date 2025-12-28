#!/bin/bash
echo "Démarrage de l'API de Gestion des Employés..."
echo ""
echo "Assurez-vous d'avoir activé votre environnement virtuel et installé les dépendances."
echo ""
uvicorn main:app --reload


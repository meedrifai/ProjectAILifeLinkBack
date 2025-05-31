#!/bin/bash

echo "🔍 Vérification pré-déploiement..."

# Vérifier que model.pkl existe
if [ ! -f "model.pkl" ]; then
    echo "❌ ERREUR: model.pkl n'existe pas dans le dossier courant!"
    echo "📁 Fichiers présents:"
    ls -la *.pkl 2>/dev/null || echo "Aucun fichier .pkl trouvé"
    exit 1
fi

echo "✅ model.pkl trouvé"
echo "📊 Taille du fichier: $(du -h model.pkl)"

# Vérifier .dockerignore
if [ -f ".dockerignore" ]; then
    echo "🔍 Vérification .dockerignore..."
    if grep -q "model.pkl" .dockerignore; then
        echo "⚠️  ATTENTION: model.pkl pourrait être ignoré dans .dockerignore"
        grep -n "model.pkl" .dockerignore
    fi
    if grep -q "\*.pkl" .dockerignore; then
        echo "⚠️  ATTENTION: *.pkl pourrait être ignoré dans .dockerignore"
        grep -n "\*.pkl" .dockerignore
    fi
fi

# Test de build local
echo "🏗️  Test de build Docker local..."
docker build -t test-backend . 

if [ $? -eq 0 ]; then
    echo "✅ Build Docker réussi"
    echo "🔍 Vérification du contenu du container..."
    # Fix pour Windows Git Bash - utiliser winpty ou double slash
    docker run --rm test-backend ls -la //app/model.pkl 2>/dev/null || \
    docker run --rm test-backend ls -la /app/model.pkl 2>/dev/null || \
    winpty docker run --rm test-backend ls -la /app/model.pkl
    if [ $? -eq 0 ]; then
        echo "✅ model.pkl présent dans le container Docker"
        echo "🚀 Prêt pour le déploiement Fly.io"
    else
        echo "❌ model.pkl ABSENT du container Docker!"
        exit 1
    fi
else
    echo "❌ Échec du build Docker"
    exit 1
fi
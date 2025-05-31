# Utiliser l'image officielle Python 3.13.3 slim
FROM python:3.13.3-slim

# Empêche les erreurs silencieuses
SHELL ["/bin/bash", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer curl (pour les health checks)
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Afficher les fichiers AVANT le COPY complet
RUN echo "=== AVANT COPY - Contenu actuel de /app ===" && ls -la /app

# Copier tous les fichiers dans le conteneur
COPY . .

# Analyse détaillée des fichiers après le COPY
RUN set -e && \
    echo "=== APRÈS COPY - Contenu de /app ===" && \
    ls -la /app && \
    echo "=== Recherche de fichiers .pkl ===" && \
    find /app -name "*.pkl" -type f -exec ls -la {} \; || echo "Aucun .pkl trouvé" && \
    echo "=== Vérification spécifique : model.pkl ===" && \
    if [[ -f "/app/model.pkl" ]]; then \
        echo "✅ model.pkl trouvé !"; \
        ls -la /app/model.pkl; \
        file /app/model.pkl; \
        du -h /app/model.pkl; \
        md5sum /app/model.pkl; \
    else \
        echo "❌ model.pkl introuvable !"; \
        find /app -type f | head -20; \
        exit 1; \
    fi

# Test de lecture Python du fichier model.pkl (corrigé)
RUN set -e && \
    echo "=== TEST DE LECTURE Python: model.pkl ===" && \
    python3 -c "import pickle, os, sys; \
print('Test de lecture model.pkl...'); \
model_path = '/app/model.pkl'; \
if os.path.exists(model_path): \
    try: \
        with open(model_path, 'rb') as f: \
            data = pickle.load(f); \
        print('✅ model.pkl LISIBLE avec succès !'); \
        print(f'Type de données: {type(data)}'); \
    except Exception as e: \
        print(f'❌ Erreur lors de la lecture de model.pkl : {e}'); \
        sys.exit(1); \
else: \
    print('❌ model.pkl introuvable lors du test Python'); \
    sys.exit(1)"

# Vérification des fichiers Python source
RUN echo "=== VÉRIFICATION DES SOURCES ===" && \
    [[ -f "chatboot.py" ]] && echo "📄 chatboot.py :" && head -20 chatboot.py || echo "❌ chatboot.py introuvable" && \
    [[ -f "main.py" ]] && echo "📄 main.py :" && head -10 main.py || echo "❌ main.py introuvable"

# Exposer le port (ex. : pour Uvicorn / FastAPI)
EXPOSE 8000

# Lancer l'application avec logs détaillés
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]

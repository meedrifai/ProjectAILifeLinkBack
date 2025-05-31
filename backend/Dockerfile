# Use official Python 3.13.3 slim image
FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Copy requirements first (pour le cache Docker)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL application files
COPY . .

# DEBUG pour Fly.io: Vérifier que tous les fichiers sont présents
RUN echo "=== DEBUG FLY.IO: Fichiers dans /app ===" && \
    ls -la /app/ && \
    echo "=== DEBUG FLY.IO: Vérification model.pkl ===" && \
    ls -la /app/model.pkl && \
    echo "=== DEBUG FLY.IO: Taille du fichier ===" && \
    du -h /app/model.pkl && \
    echo "=== DEBUG FLY.IO: Test de lecture ===" && \
    python3 -c "import pickle; print('✅ model.pkl lisible')" 2>/dev/null || echo "❌ Erreur lecture model.pkl"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
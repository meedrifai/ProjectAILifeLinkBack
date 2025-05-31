# Use official Python 3.13.3 slim image
FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model.pkl EXPLICITEMENT en premier
COPY model.pkl /app/model.pkl

# Vérifier que model.pkl est copié
RUN ls -la /app/model.pkl && \
    echo "✅ model.pkl copié avec succès"

# Copy other files
COPY *.py /app/
COPY . .

# Vérification finale
RUN ls -la /app/ && \
    test -f /app/model.pkl && \
    echo "✅ model.pkl présent et prêt"

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
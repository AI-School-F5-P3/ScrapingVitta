# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las herramientas necesarias para compilar dependencias
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copia los archivos de requisitos en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de tu proyecto en el contenedor
COPY . .

# Exponer un puerto si tu aplicación lo requiere (no es necesario para Scrapy)
EXPOSE 8000

# Comando por defecto para ejecutar cuando el contenedor se inicie
CMD ["scrapy", "crawl", "quotes"]
#CMD ["streamlit", "run", "app.py"]

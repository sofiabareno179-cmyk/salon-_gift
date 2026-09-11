# Usa una imagen de Python basada en Alpine
FROM python:3.12-alpine

# Instala las herramientas de compilación necesarias
RUN apk add --no-cache \
    build-base \
    linux-headers \
    gcc \
    musl-dev

# Establece el directorio de trabajo
WORKDIR /workspace

# Copia el archivo de requerimientos
COPY ["salon gift/requirements.txt", "requirements.txt"]

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia la aplicación
COPY ["salon gift", "."]

# Crea el directorio de subida de imágenes de servicios
RUN mkdir -p app/static/uploads/servicios

EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python", "run.py"]
# Usa una imagen de Python basada en Alpine
FROM python:3.12-alpine

# Instala git y las herramientas de compilación necesarias
RUN apk add --no-cache \
    git \
    build-base \
    linux-headers \
    gcc \
    musl-dev \
    postgresql-dev \
    libpq

WORKDIR /workspace

# Clona el repositorio en build time y coloca la aplicación en /workspace/app_src
# (funciona sin necesidad de build context: Coolify solo envía el Dockerfile)
RUN git clone --depth 1 --branch main \
        https://github.com/sofiabareno179-cmyk/salon-_gift.git /repo \
    && (cp -r /repo/salon_gift /workspace/app_src || cp -r "/repo/salon gift" /workspace/app_src) \
    && rm -rf /repo

WORKDIR /workspace/app_src

# Instala las dependencias
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Creamos el directorio de subida de imágenes de servicios
RUN mkdir -p app/static/uploads/servicios

EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python", "run.py"]
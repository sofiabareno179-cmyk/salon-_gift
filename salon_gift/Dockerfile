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

# La URL del repo se puede anular en Coolify (Build Arg) para no depender de una rama cacheada
ARG REPO_URL=https://github.com/sofiabareno179-cmyk/salon-_gift.git
ARG REPO_BRANCH=main

# Clona el repositorio en build time y coloca la aplicación en /workspace/app_src
# (funciona sin necesidad de build context: Coolify solo envía el Dockerfile)
RUN git clone --depth 1 --branch "${REPO_BRANCH}" "${REPO_URL}" /repo \
    && (cp -r /repo/salon_gift /workspace/app_src || cp -r "/repo/salon gift" /workspace/app_src) \
    && rm -rf /repo

WORKDIR /workspace/app_src

# Para que los logs aparezcan en Coolify sin buffering
ENV PYTHONUNBUFFERED=1

# Instala las dependencias
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Creamos el directorio de subida de imágenes de servicios
RUN mkdir -p app/static/uploads/servicios

EXPOSE 5000

# Healthcheck para que Coolify reporte estado y no muestre 404 cuando la app cae
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=5)" || exit 1

# Ejecuta la aplicación Flask
CMD ["python", "run.py"]
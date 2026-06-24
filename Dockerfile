FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

<<<<<<< Updated upstream
COPY ["salon gift/requirements.txt", "requirements.txt"]
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ["salon gift", "."]
=======
# Install dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . ./

>>>>>>> Stashed changes
RUN mkdir -p app/static/uploads/servicios

EXPOSE 5000

CMD ["python", "run.py"]

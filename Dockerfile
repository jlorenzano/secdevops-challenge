# Imagen de python
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Copiado e instalacion de las dependencias necesarias para la ejecion de la api
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiado del archivo de variables de entorno
#COPY .env .

# Copiado del codigo fuente
COPY ./app ./app

# Puerto que usara el contenedor que se ejecute a partir de esta imagen
EXPOSE 8000

# Comando de ejecucion de uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

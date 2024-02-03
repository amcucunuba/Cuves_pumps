# Usa la imagen oficial de Python como imagen base
FROM python:3.9.6

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al directorio de trabajo
COPY ./esp_app /app/esp_app
COPY ./esp_app/assets /app/assets
COPY ./requirements.txt /app/

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Define el punto de entrada para el contenedor
CMD ["python", "esp_app/app_esp.py", "runserver", "0.0.0.0:8000"]


# Usa la imagen oficial de Python como imagen base
FROM  python:3.9.6

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al directorio de trabajo
COPY ./esp_app /app/esp_app
COPY ./esp_app /app/app_esp

# Instala las dependencias de la aplicación
RUN pip install tus_dependencias

# Define el punto de entrada para el contenedor
CMD ["python", "esp_app/app_esp.py", "runserver", "0.0.0.0:8000"]
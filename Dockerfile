# Usa la imagen oficial de Python como imagen base
FROM python:3.9


RUN apt-get update && \
    apt-get install -y uwsgi

# Establece el directorio de trabajo en el contenedor
WORKDIR /app
# Copia los archivos de la aplicación
COPY ./app_flask /app
COPY ./app_flask/assets /assets
COPY requirements.txt .
# Instala las dependencias de Python
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Añade la instalación de Pandas
RUN pip3 install pandas 

# Configura el comando predeterminado para ejecutar uWSGI con el archivo uwsgi.ini
EXPOSE 80
CMD gunicorn -b 0.0.0.0:80 --timeout 300 app:server 
# Usa la imagen oficial de Python como imagen base
FROM python:3.9

RUN apt-get update
RUN apt-get install nano
RUN apt-get update && apt-get install -y uwsgi

# Establece el directorio de trabajo en el contenedor
RUN mkdir wd
WORKDIR /app/
COPY ./esp_app /app/esp_app
COPY ./esp_app/assets /app/assets
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Añade la instalación de Pandas
RUN pip3 install pandas 


CMD [ "uwsgi", "--http=0.0.0.0:80", "--wsgi-file=app.py", "--callable=app_esp" ]

RUN apt-get clean && rm -rf /var/lib/apt/lists/*


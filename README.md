# Web Scraping App con Scrapy y SQLite Para XYZ Corp
## Descripción
Esta es una aplicación de web scraping desarrollada con Scrapy, una herramienta de scraping potente y versátil. La aplicación está diseñada para extraer datos de sitios web específicos y almacenar la información recolectada en una base de datos SQLite. Además, se generan logs detallados del proceso de scraping para facilitar el monitoreo y la depuración.

## Requisitos
Antes de ejecutar la aplicación, asegúrate de tener instaladas las siguientes dependencias:

* Python 3.6+
* Scrapy
* SQLite

## Ejecución
Para ejecutar la aplicación de scraping, utiliza el siguiente comando en la terminal:

* 1- Cargamos la base de datos
~~~
    scrapy crawl quotes
~~~
* 2- En el directorio donde este app.py ejecutamos:
~~~
    streamlit run app.py
~~~
## Instrucciones para Ejecutarlo con Docker
* 1 Instalamos Docker:
    - Sigue las instrucciones en [Docker](https://docs.docker.com/get-docker/) para instalar Docker en tu sistema.
* 2 Obtenemos la imagen Docker:
    - Si has construido la imagen localmente, usa el siguiente comando para construirla:
  ~~~
  docker build -t mi-aplicación-scrapy .
  ~~~
    - También podemos ejecutarlo desde Docker Hub, usamos:
  ~~~
  docker pull sweetvitta/scrapyvitta:v1.1
  ~~~
* 3 Ejecutamos el contenedor:
   ~~~
   docker run mi-aplicación-scrapy
   ~~~


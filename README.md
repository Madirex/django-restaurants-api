# django-restaurants-api

Este proyecto es una API desarrollada en Django para gestionar la información de restaurantes, menús, reservas, pedidos y más.

[Ir al proyecto del frontend (desarrollado en Vue 3)](https://github.com/Madirex/vue-restaurants-front/)

## ✏️ Instalación previa (requisitos)
Es importante crear una carpeta .envs y dentro un archivo .env con el siguiente contenido:

    POSTGRES_DB=restaurants
    POSTGRES_USER=madi
    POSTGRES_PASSWORD=#T\MzF]qe:z4#tt#
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

Se deberá reemplazar los valores de POSTGRES_USER y POSTGRES_PASSWORD por los valores deseados.

Además, se deberá de tener Docker instalado y en ejecución.

## Comandos

#### Para ejecutar los tests

    docker exec restaurants-web-1 bash -c "python manage.py test"

#### Para ejecutar todo por primera vez y hacer las migraciones

    docker-compose up -d && sleep 1 &&
    docker exec restaurants-web-1 bash -c "python manage.py makemigrations" &&
    docker exec restaurants-web-1 bash -c "python manage.py migrate"

#### Para ejecutar todo
    
    docker-compose up -d

#### Para eliminar todo

⚠️ Antes de ejecutar este comando, ten en cuenta que eliminará todos los datos y volúmenes relacionados con el proyecto.

    docker-compose down -v --remove-orphans


## Diagrama UML
![Tests](/images/UML.png)

## Dependencias

- **django==3.2.4**: El framework web utilizado para el desarrollo del proyecto.
- **Markdown==3.1.1**: Para procesar texto en formato Markdown.
- **django-filter==2.0.0**: Para filtrar consultas en la API.
- **djangorestframework==3.12.2**: Herramientas adicionales para construir APIs web.
- **Werkzeug>=2.0.0**: Librería WSGI utilizada por Django.
- **django-extensions>=3.2**: Extensiones útiles para el desarrollo en Django.
- **pyOpenSSL>=23.0.0**: Para soporte de SSL/TLS.
- **psycopg2==2.9.9**: Adaptador de base de datos PostgreSQL para Django.
- **django-ckeditor==5.9.0**: Integración de CKEditor en Django.
- **Pillow==7.1.2**: Librería para procesamiento de imágenes en Django.
- **itsdangerous==2.1.0**: Herramientas para seguridad y cifrado en Flask.
- **django-cors-headers==3.9.0**: Habilita el manejo de solicitudes CORS en Django.

## Descripción del Proyecto

El proyecto consiste en una API de restaurantes que permite gestionar la información de varios aspectos, incluyendo:

- **Calendarios y Horarios**: Cada restaurante tiene calendarios con horarios estacionales, días excluidos y días excepcionales.
- **Enlaces Restaurante-Plato**: Relaciona un restaurante con sus platos.
- **Reservas y Pedidos**: Funcionalidades para realizar reservas y pedidos.
- **Menú del Restaurante**: Grupos de platos que conforman el menú de un restaurante.
- **Certificado SSL**: Integración de certificados SSL para seguridad en las comunicaciones.
- **Categorías de Plato**: Categorización de platos para facilitar su gestión.
- **Códigos de Descuento**: Utilizados en pedidos para aplicar descuentos especiales.

## Pruebas

Se han realizado un total de 147 tests para garantizar el correcto funcionamiento del proyecto.

![Tests](/images/tests.png)

## Documentación Adicional

- Se ha proporcionado una colección de Postman: restaurants-rest.postman_collection.json, para facilitar la interacción con la API.

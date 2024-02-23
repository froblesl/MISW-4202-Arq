# MISW-4202-Arquitecturas ágiles de software

El experimento desarrollado busca comprobar cuantos usuarios se pueden registrar simultaneamente en el sistemas SportApp.

La arquitectura del proyecto consta de:

Un API Gateway que recibe las peticiones y las distribuye al microservicio de registro. (Nginx)
Un sistema de mensajería que permite la comunicación entre el API Gateway y el microservicio de registro. (Celery y Redis)
Un microservicio de registro con su propia base de datos que recibe las peticiones de registro y las procesa. (Flask y SQLite)
Un sistema de monitoreo que permite visualizar el estado del servidor en tiempo real. (Nginx)

## Requisitos

- Python 3.8
- Redis
- Nginx
- Docker
- Docker Compose
- Pip
- Brew
- Gunicorn
- Celery
- Flask
- SQLite
- Postman
- Jmeter

## Instalación

Instalar en la maquina local redis, se puede obtener de la siguiente URL: https://redis.io/download

Descargar el codigo fuente del proyecto.

Ubicarse en la carpeta flaskr y ejecutar el siguiente comando para instalar las dependencias del proyecto:

Crear un ambiente virtual con el siguiente comando:

En Windows:
```bash
python -m venv venv
```

En Mac:
```bash
python3 -m venv venv
```

Activar el ambiente virtual con el siguiente comando:

En Windows:
```bash
venv\Scripts\activate
```

En Mac:
```bash
source venv/bin/activate
```

Instalar las dependencias del proyecto con el siguiente comando:

```bash
pip install -r requirements.txt
```

Instalar en la maquina local nginx, se puede obtener de la siguiente URL: https://nginx.org/en/download.html

Modificar el archivo nginx.conf garantizando que contenga el codigo del archivo nginx.conf y reiniciar el servicio de nginx

En Windows:
```bash
nginx -s reload
```

En Mac:
```bash
brew services restart nginx
```

Asegurarse que el servicio de redis este corriendo.
Asegurarse que el servicio de nginx este corriendo.

## Ejecución

Para ejecutar el proyecto se debe correr el siguiente comando en la raíz del proyecto (para e caso del ejemplo se esta corriendo con 50 hilos, la cantidad de hilos definida depende de la capacidad de la maquina donde se va a ejecutar el proyecto):

```bash
gunicorn -w 50 -b :5000 flaskr.app:app
```

Para ejecutar el sistema de mensajería se debe correr el siguiente comando en la raíz del proyecto:

```bash
celery -A flaskr.tasks worker --loglevel=info -Q signin_task -c1
```

## Pruebas

Se pueden hacer peticiones desde postman o jmeter y validar resultado en la base de datos. Para realizar las peticiones se debe tener en cuenta que el endpoint es http://localhost:8080/signup y el body de la petición debe ser un json con los siguientes campos:

```json
{
    "usuario": "usuario",
    "password": "password",
    "nombre": "nombre",
    "telefono": "telefono",
    "correo": "correo"
}
```

## Monitoreo

El estado del servidor se puede visualizar en tiempo real en el sistema de monitoreo. Para acceder al sistema de monitoreo se debe ingresar a la url: http://localhost:8080/nginx_status



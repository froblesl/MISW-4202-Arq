# MISW-4202-Arquitecturas ágiles de software
Instalar en la maquina local celery y redis

pip install celery -s
brew services start redis 

Instalar en la maquina local nginx
brew services start nginx

modificar el archivo /usr/local/etc/nginx/nginx.conf en la sección server garantizando que contenga el codigo del archivo nginx-proxy.conf y reiniciar el servicio de nginx

```
Instalar ambiente virtual

python3 -m venv venv

subir ambiente virtualizado en dos consolas diferentes

source venv/bin/activate  

correr en ambiente virtualizado en la carpeta flaskr: flask run
correr en otra terminal en la raíz del proyecto: celery -A flaskr.tasks worker --loglevel=info -Q signin_task

validar que redis y nginx esten corriendo

hacer peticiones desde postman o jmeter y validar resultado bdd

el monitor se consulta en la url: http://localhost:8080/nginx_status

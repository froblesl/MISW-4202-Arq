FROM python:3.9.6
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . /app/flaskr/
WORKDIR /app/flaskr/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
#CMD [ "bash" ]

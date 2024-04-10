FROM python:3.11-alpine

COPY . /code

WORKDIR /code

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python manage.py migrate

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

EXPOSE 8000
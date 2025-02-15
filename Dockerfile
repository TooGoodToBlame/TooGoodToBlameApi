FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["./entrypoint.sh"]

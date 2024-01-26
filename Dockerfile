# Bazuj na obrazie Pythona
FROM python:3.11

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik z zależnościami i zainstaluj je
COPY requirements.txt .
RUN pip install -r requirements.txt

# Skopiuj kod źródłowy aplikacji Django
COPY . /app
# Ustaw skrypt jako ENTRYPOINT
ENTRYPOINT ["./entrypoint.sh"]

# CMD ["python3", "manage.py", "migrate"]
# Uruchom Gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "too_good_to_blame.wsgi:application"]

FROM python:3.12.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /maxsport

RUN apt-get update && apt-get install -y \
    gcc \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN useradd -ms /bin/bash djangouser
USER djangouser


# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["gunicorn", "-w", "4", "MaxSports.wsgi:application", "-b", "0.0.0.0:8000"]

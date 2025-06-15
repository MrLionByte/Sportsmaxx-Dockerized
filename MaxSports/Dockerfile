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

RUN mkdir -p /maxsport/staticfiles && chown -R 1000:1000 /maxsport/staticfiles

RUN useradd -ms /bin/bash djangouser
USER djangouser

COPY --chown=djangouser:djangouser entrypoint.sh /maxsport/entrypoint.sh

ENTRYPOINT ["/maxsport/entrypoint.sh"]

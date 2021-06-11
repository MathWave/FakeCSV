FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE FakeCSV.settings
RUN mkdir -p /app/
WORKDIR /app/
COPY . /app/
RUN pip install -r requirements.txt
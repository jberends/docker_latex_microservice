FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY ./requirements.txt /requirements.txt

RUN pip install -U -r /requirements.txt

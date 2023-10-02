FROM python:3.9

COPY ./src /app/src/
COPY ./data /app/data/
COPY ./requirements.txt /app
COPY ./run.sh /app

WORKDIR /app

RUN python -m pip install --upgrade pip && python -m pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["/bin/bash", "run.sh"]
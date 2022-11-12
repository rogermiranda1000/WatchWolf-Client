FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 7000

CMD [ "python3", "ClientsManager.py"]

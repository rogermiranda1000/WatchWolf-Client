FROM nikolaik/python-nodejs
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 7000-7100

CMD [ "python3", "ClientsManager.py"]

FROM nikolaik/python-nodejs
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements.py requirements.py
RUN pip3 install -r requirements.txt
RUN npm install --save mineflayer-pathfinder
RUN python3 requirements.py

COPY . .

EXPOSE 7000-7199

CMD [ "python3", "ClientsManager.py"]

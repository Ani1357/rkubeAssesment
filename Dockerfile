FROM python:3.11-slim-buster

WORKDIR /usr/scr/app

COPY requirements.txt requirements.txt
COPY app.py app.py
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

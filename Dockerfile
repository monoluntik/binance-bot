FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main_bot.py" ]
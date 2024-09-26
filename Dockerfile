FROM python:alpine

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "-m", "bot.main"]
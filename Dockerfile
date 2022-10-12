FROM python:3.7

WORKDIR /Dinning_Hall

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "./server.py"]
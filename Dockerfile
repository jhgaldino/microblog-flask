FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Initialize the database and apply migrations
RUN flask db init || true && flask db migrate || true && flask db upgrade

CMD ["python", "run.py"]

FROM python:alpine
RUN apk add --no-cache bash postgresql-client
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main_sqlalchemy:app --host 0.0.0.0 --port 8000 --reload"]

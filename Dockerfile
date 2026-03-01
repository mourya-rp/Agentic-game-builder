
FROM python:3.13-slim


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


VOLUME /app/generated_game


CMD ["python", "main.py"]
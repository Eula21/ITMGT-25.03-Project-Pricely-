FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir --timeout=60 --retries=5 --resume-retries=3 -r requirements.txt -i https://pypi.org/simple

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

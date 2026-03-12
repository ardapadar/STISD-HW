FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn python-jose[cryptography] python-multipart
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
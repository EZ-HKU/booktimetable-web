FROM python:3.9.18-alpine3.18
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt
    
CMD ["python", "src/web.py"]
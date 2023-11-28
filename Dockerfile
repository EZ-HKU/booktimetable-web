FROM python:3.9.18-alpine3.18
COPY . /app
WORKDIR /app
# install dependencies with no cache
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 443
CMD ["python", "src/web.py"]
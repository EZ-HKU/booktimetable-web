# HKU library facilities auto-booking website

## Deployment
### 1. Prerequisites
Make sure you have installed `docker` and `docker-compose` on your server.
### 2. Pull the code
```bash
git clone https://github.com/EZ-HKU/booktimetable-web.git
```
### 3. Set the environment
```bash
# set environment variables
export MONGO_LINK=<your mongo link>
export BOOK_PW=<your booking password>
```
### 4. Prepare ssl certificate files
```bash
# put ssl certificate files in key folder
cd booktimetable-web
mkdir key
cp <your key file> key/key.pem
cp <your cert file> key/cert.pem
```
### 5. Run the code with docker compose
```bash
docker-compose up -d
```
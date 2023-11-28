# HKU library facilities auto-booking website

## Deployment
### 1. Pull the code
```bash
git clone https://github.com/adlsdztony/booktimetable-web.git
```
### 2. Prepare the environment
```bash
# set environment variables
export MONGO_LINK=<your mongo link>
export BOOK_PW=<your booking password>
```
### 3. Put ssl certificate files
```bash
# put ssl certificate files
mkdir key
cp <your key file> key/key.pem
cp <your cert file> key/cert.pem
```
### 4. Run the code with docker compose
```bash
docker-compose up -d
```
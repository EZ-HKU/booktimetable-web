# HKU library facilities auto-booking website
> The website is extracted from a private project [autobook](https://github.com/adlsdztony/autobook).

> NOTE: This website only add tasks to the database, you should book the tasks regularly with other scripts. ( e.g. [hkulibrary](https://github.com/adlsdztony/hkulibrary) )

## Deployment
### 1. Prerequisites
* Make sure you have installed `docker` and `docker-compose` on your server.
* Make sure you have a `mongo database`.
* Make sure you have a `ssl certificate` for your domain.
* Make sure you have opened port `80` and `443` on your server.

### 2. Pull the code
```bash
git clone https://github.com/EZ-HKU/booktimetable-web.git
```
### 3. Set the environment
```bash
# set environment variables
export MONGO_LINK=<your mongo link>
export BOOK_PW=<the secret key for flask app (can be any string)>
```
### 4. Prepare ssl certificate files
```bash
# put ssl certificate files in key folder
cd booktimetable-web
mkdir key
cp <your key file> key/key.pem
cp <your cert file> key/cert.pem
```
### 5. Run with docker compose
```bash
docker-compose up -d
```
## **For developers**
### 1. Prerequisites
* Make sure you have installed `docker` and `docker-compose` on your server.
* Make sure you have opened port `8080` on your server.
### 2. Pull the code
```bash
git clone https://github.com/EZ-HKU/booktimetable-web.git
```
### 3. Run with docker compose
```bash
cd booktimetable-web
docker-compose -f docker-compose-dev.yml up -d
```
Now you can visit the website at `http://<your server ip>:8080`.

The default username and password is `admin` and `123456`.
# How to?

* Create .env file
```bash
# BACKEND SETTINGS
### POSTGRES SETTINGS
export PG_HOST=
export PG_PORT=
export PG_DBNAME=
export PG_USER=
export PG_PASSWORD=

### JWT SETTINGS
export JWT_SECRET_KEY=
export JWT_ALGORITHM=
export JWT_ACCESS_TOKEN_EXPIRE_MINUTES=

# FRONTEND SETTINGS
export BACKEND_USERNAME=
export BACKEND_PASSWORD=
export BACKEND_URL=
```
* Create docker containers for frontend and backend(see docker-compose.yaml)
```bash
docker compose up
```

# See our WebService deployed in Yandex Cloud
[AI Safety Leaderboard](http://84.201.151.208:7860/)
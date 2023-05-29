Please, create in main folder .env

POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB_NAME=postgres_db_name
POSTGRES_DOMAIN=localhost
POSTGRES_PORT=port

URI=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_DOMAIN}:${POSTGRES_PORT}/${POSTGRES_DB_NAME}

SECRET_KEY=secret
ALGORITHM=algorithm

MAIL_USERNAME=example@example.ua
MAIL_PASSWORD=mail_password
MAIL_FROM=example@example.ua
MAIL_PORT=port
MAIL_SERVER=mail_server

REDIS_HOST=redis_host
REDIS_PORT=port

CLOUDINARY_NAME=name
CLOUDINARY_API_KEY=key
CLOUDINARY_API_SECRET=secret


To start testing:

pytest --cov=. --cov-report html tests/




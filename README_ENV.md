Using environment variables securely

Quick steps to run/build without hardcoding secrets:

1. Copy `.env.example` to `.env` and fill real values (do NOT commit `.env`).

2. Local run (Windows cmd):

```bat
# set environment from .env (example using a small helper like "dotenv" is optional)
# For cmd.exe, you can set variables manually or use a powershell or a tool to load .env
set DATABASE_URL=postgresql://user:password@host:5432/dbname
set SECRET_KEY=your_secret_key
python app.py
```

3. Using Docker (recommended):

# Build image
```bat
docker build -t spam-classifier -f dockerfile .
```

# Run container with env file
```bat
docker run --env-file .env -p 5000:5000 spam-classifier
```

4. Using Docker Compose (recommended for dev with Postgres): create a `docker-compose.yml` and mount .env or pass variables. Using Compose keeps the database and the app isolated and avoids embedding secrets in images.

Notes:
- Keep `.env` private. Use secret managers for production (AWS Secrets Manager, Azure Key Vault, etc.).
- Do not commit PEM keys or `.env` to source control. Use the `.gitignore` included.

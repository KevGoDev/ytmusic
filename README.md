# Personal flask template
## Secrets
`src/.env` should have the following secrets:
```
DATABASE_URL=...
```

## Database migrations
```
alembic revision --autogenerate -m "1"
alembic upgrade head
```

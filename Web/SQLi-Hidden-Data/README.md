# IITCTF — SQL Injection: Hidden Data

Modern university inventory console for an authorized SQL injection CTF.

## Run

```bash
docker compose up --build
```

Open:

`http://127.0.0.1:8083`

## Objective

The `productId` parameter is intentionally concatenated into a SQL query.
Some catalog records are hidden from the normal view. Exploit the SQL
injection to retrieve the hidden record and the runtime-generated flag.

Flag format: `IITCTF{...}`

The flag is generated at application startup and is not stored in the source.

## Cleanup

```bash
docker compose down
```

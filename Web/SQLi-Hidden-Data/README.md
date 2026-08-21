# IITCTF — SQL Injection: Hidden Data

University Store

Welcome to the university's internal store portal. Students can check the availability of products using the provided product ID.

The portal appears to work normally, but the way product information is processed may not be as secure as it seems. Some products are hidden from the regular inventory view.

Can you manipulate the product search functionality to access the hidden inventory and retrieve the flag?

Objective: Exploit the SQL injection vulnerability and retrieve the hidden product and flag.

Difficulty: Easy

Category: Web / SQL Injection

Flag Format: IITCTF{...}

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

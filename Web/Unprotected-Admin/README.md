# IITCTF — Unprotected Admin Functionality

A local Docker CTF challenge inspired by the unprotected-administration access-control scenario.

## Run

```bash
docker compose up --build
```

Open `http://127.0.0.1:8081`.

## Intended discovery

The homepage does **not** contain a link to `robots.txt`.

Visit it directly:

`http://127.0.0.1:8081/robots.txt`

It returns:

```text
User-agent: *
Disallow: /admin
```

Then inspect the disallowed path:

`http://127.0.0.1:8081/admin`

The `/admin` endpoint is intentionally unprotected and displays a runtime-generated IITCTF flag.

The flag is generated with Python `secrets` when the application starts and is not committed to Git.

This is a fictional university-style CTF interface and is not an official University of Dhaka website.

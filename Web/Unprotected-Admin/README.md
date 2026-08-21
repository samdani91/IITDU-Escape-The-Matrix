# IITCTF — Unprotected Admin Functionality

Welcome to the university's student portal. Students can log in using their university-provided ID and password to access their academic information and services.

However, the portal also has a super administrator account with access to functionality that regular students cannot use.

Can you discover the administrator's account and access the restricted functionality?

Objective: Gain access to the administrator area and retrieve the flag.

Difficulty: Easy
Category: Web / Access Control
Flag Format: IITCTF{...}

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

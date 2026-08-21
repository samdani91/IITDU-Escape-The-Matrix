# IITCTF — Banking Under Pressure (Corrected)

**Category:** Web / Business Logic / BOLA / Race Condition  
**Difficulty:** Upper-Medium  
**Flag:** `IITCTF{...}`

## Scenario

NovaBank is a fictional training bank. A student can register, log in, deposit fictional funds, and transfer money to another username.

The challenge contains two intentional vulnerabilities:

1. **BOLA / IDOR** — authenticated users can request transaction/profile data for another numeric account ID.
2. **Race condition** — the transfer balance check and balance update are not atomic. Concurrent transfers can reuse the same observed balance.

The vulnerabilities are intentional and isolated to this local CTF application.

## Start

```bash
docker compose down
docker rm -f iitctf-banking-under-pressure 2>/dev/null || true
docker compose up --build
```

Open:

`http://127.0.0.1:8084`

Training login:

- Username: `student`
- Password: `student123`

## Intended solve path

### 1. Enumerate the API

Use Burp Proxy/HTTP history while browsing the dashboard.

Useful endpoints:

- `GET /api/profile/<account_id>`
- `GET /api/transactions/<account_id>`

The application intentionally does not verify that the requested account belongs to the logged-in user.

### 2. Discover account information

Try numeric account IDs as an authenticated user.

`/robots.txt` also gives a small discovery hint.

Account 3 is the operations account.

### 3. Analyze the transfer request

Normal transfer:

```http
POST /transfer
Content-Type: application/x-www-form-urlencoded

recipient=campus_store&amount=9999
```

A normal request cannot repeatedly spend the original balance because the balance is only 10,000.

### 4. Trigger the race

Send multiple identical transfer requests concurrently through Burp.

A practical target is:

```text
recipient=campus_store
amount=9999
```

Use Burp Repeater's parallel/group sending capability, or another local request generator, and send enough concurrent requests to make the campus store's cumulative balance reach 50,000 BDT.

Because each request can read the same starting balance before the delayed update, several requests can pass the check.

### 5. Retrieve the flag

After the race condition succeeds, return to the dashboard.

The application displays the challenge flag after the campus store balance reaches the threshold.

## Why the original version was unstable

The previous lab used SQLite for concurrent operations. During parallel testing it could produce:

`sqlite3.OperationalError: database is locked`

That is an implementation problem, not the intended vulnerability.

This corrected version uses deterministic in-memory state with a short controlled delay, so the race condition can be reproduced without SQLite locking errors.

## Reset

The state is in memory. Restarting the container resets the challenge:

```bash
docker compose down
docker compose up --build
```

## Author notes

The application is deliberately vulnerable. Do not deploy it as a real banking application.

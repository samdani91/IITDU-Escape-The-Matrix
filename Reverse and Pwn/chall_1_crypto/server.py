import socket
import json
import threading
import hashlib
import os
import time
from itertools import permutations

# ==============================
# Configuration
# ==============================
HOST = "34.93.127.41"
PORT = 5016

POW_DIFFICULTY = "00000"   # number of leading hex zeros
POW_TIME_LIMIT = 25      # seconds

# ==============================
# Load graph
# ==============================
edges = []
with open("graph.txt") as f:
    for line in f:
        u, v = map(int, line.split())
        edges.append((u, v))

NODES = max(max(u, v) for u, v in edges) + 1

# ==============================
# Load secret coloring
# ==============================
with open("secret_coloring.txt") as f:
    secret = [int(x.strip()) for x in f]

assert len(secret) == NODES

# ==============================
# Crypto bait: salts + commitments
# ==============================
salts = [os.urandom(16) for _ in range(NODES)]
commits = [
    hashlib.sha256(bytes([secret[i]]) + salts[i]).hexdigest()
    for i in range(NODES)
]

# ==============================
# Proof-of-Work
# ==============================
def do_pow(conn):
    challenge = os.urandom(8).hex()
    start = time.time()

    msg = (
        f"This your POW: {challenge}\n"
        f"Find x such that sha256(challenge + x) starts with {POW_DIFFICULTY}\n"
        f"Work fast!!!!\n\n"
        f"Submit x:\n"
    )
    conn.sendall(msg.encode())

    conn.settimeout(POW_TIME_LIMIT)

    try:
        x = conn.recv(1024).strip()
    except socket.timeout:
        return False

    if not x:
        return False

    elapsed = time.time() - start
    if elapsed > POW_TIME_LIMIT:
        return False

    h = hashlib.sha256((challenge + x.decode()).encode()).hexdigest()
    return h.startswith(POW_DIFFICULTY)

# ==============================
# Client handler
# ==============================
def handle_client(conn):
    try:
        # ---- PoW gate ----
        if not do_pow(conn):
            conn.sendall(b"Invalid or expired PoW\n")
            conn.sendall(b"Bye....\n")
            conn.close()
            return

        conn.settimeout(None)
        conn.sendall(b"Welcome to Coloring Heist!\n")
        conn.sendall(b"Enter JSON request (newline terminated):")

        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                req = json.loads(data.decode())
            except:
                continue

            # ---- Query endpoint (crypto bait) ----
            if req.get("option") == "query":
                u, v = req["edge"]
                resp = {
                    "proofs": [
                        {"color": secret[u], "salt": salts[u].hex()},
                        {"color": secret[v], "salt": salts[v].hex()},
                    ]
                }
                conn.sendall(json.dumps(resp).encode() + b"\n")

            # ---- Guess endpoint (real logic) ----
            elif req.get("option") == "guess":
                guess = req["coloring"]

                if len(guess) != NODES:
                    conn.sendall(b'{"error":"invalid length"}\n')
                    continue

                for perm in permutations([0, 1, 2]):
                    if all(perm[guess[i]] == secret[i] for i in range(NODES)):
                        conn.sendall(
                            b'{"flag":"EWUCSC{GR4Ph$-W17h-CrYp70_15_jU57_3V!L}"}\n'
                        )
                        conn.close()
                        return

                conn.sendall(b'{"error":"incorrect guess"}\n')

    except Exception:
        pass

    conn.close()

# ==============================
# Server loop
# ==============================
def main():
    print(f"[+] Coloring Heist server listening on port {PORT}")
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, _ = s.accept()
        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()

if __name__ == "__main__":
    main()


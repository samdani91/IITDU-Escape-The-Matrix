import random

N = 500
TARGET_EDGES = 10_000
SEED = 1337
random.seed(SEED)

# Step 1: random secret coloring
secret_colors = [random.randint(0, 2) for _ in range(N)]

# Step 2: list all valid edges (different colors)
candidates = []
for u in range(N):
    for v in range(u + 1, N):
        if secret_colors[u] != secret_colors[v]:
            candidates.append((u, v))

print(f"[+] Possible valid edges: {len(candidates)}")

if len(candidates) < TARGET_EDGES:
    raise ValueError("Not enough valid edges to reach target!")

# Step 3: shuffle and select
random.shuffle(candidates)
edges = candidates[:TARGET_EDGES]

# Step 4: write graph.txt
with open("graph.txt", "w") as f:
    for u, v in edges:
        f.write(f"{u} {v}\n")

# Step 5: save secret coloring
with open("secret_coloring.txt", "w") as f:
    for c in secret_colors:
        f.write(str(c) + "\n")

print("[✓] graph.txt generated successfully")


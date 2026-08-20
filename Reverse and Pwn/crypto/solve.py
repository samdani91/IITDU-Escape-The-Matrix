import sys
sys.setrecursionlimit(5000)

# Load graph
edges = []
with open("graph.txt") as f:
    for line in f:
        u, v = map(int, line.split())
        edges.append((u, v))

N = max(max(u, v) for u, v in edges) + 1
adj = [[] for _ in range(N)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

def dsatur_3color():
    colors = [-1] * N
    neigh_colors = [set() for _ in range(N)]
    uncolored = set(range(N))

    def pick_node():
        return max(uncolored, key=lambda v: (len(neigh_colors[v]), len(adj[v])))

    def backtrack():
        if not uncolored:
            return True
        v = pick_node()
        for c in range(3):
            if c in neigh_colors[v]:
                continue
            colors[v] = c
            uncolored.remove(v)
            affected = []
            for u in adj[v]:
                if colors[u] == -1 and c not in neigh_colors[u]:
                    neigh_colors[u].add(c)
                    affected.append(u)
            if backtrack():
                return True
            colors[v] = -1
            uncolored.add(v)
            for u in affected:
                neigh_colors[u].remove(c)
        return False

    assert backtrack()
    return colors

colors = dsatur_3color()
print(colors)


import sys
sys.setrecursionlimit(1 << 25)
from collections import defaultdict, deque


input = sys.stdin.readline

def read_ints():
    return list(map(int, input().split()))

n, K, X = map(int, input().split())
a = [0] + read_ints()  # 1-indexed

g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

removed = [False] * (n + 1)
sub_size = [0] * (n + 1)

def dfs_size(u, p):
    sub_size[u] = 1
    for v in g[u]:
        if v != p and not removed[v]:
            dfs_size(v, u)
            sub_size[u] += sub_size[v]

def find_centroid(u):
    dfs_size(u, -1)
    tot = sub_size[u]
    parent = -1
    changed = True
    centroid = u
  
    def dfs_find(u, p):
        for v in g[u]:
            if v != p and not removed[v]:
                if sub_size[v] > tot // 2:
                    return dfs_find(v, u)
        return u
    return dfs_find(u, -1)

def collect(u, p, dist, xr, vec):
    if dist > K:
        return
    vec.append((dist, xr))
    for v in g[u]:
        if v != p and not removed[v]:
            collect(v, u, dist + 1, xr ^ a[v], vec)

ans = 0

def decompose(start):
    global ans
    c = find_centroid(start)
    removed[c] = True

    freq_by_dist = [defaultdict(int) for _ in range(K + 1)]
    freq_by_dist[0][0] = 1  

    for v in g[c]:
        if removed[v]:
            continue
        vec = []
        collect(v, c, 1, a[v], vec)  
        for (d, xr) in vec:
            max_other = K - d
            if max_other < 0:
                continue
           
            target = xr ^ a[c] ^ X
            
            for dd in range(0, max_other + 1):
                ans += freq_by_dist[dd].get(target, 0)
        
        for (d, xr) in vec:
            if d <= K:
                freq_by_dist[d][xr] += 1

    for v in g[c]:
        if not removed[v]:
            decompose(v)

    removed[c] = False  
    removed[c] = True

decompose(1)

print(ans)

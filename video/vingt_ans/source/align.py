import re, json, math, sys
W = sys.argv[1]
text = open(W + '/script.txt', encoding='utf-8').read().split()
# attach standalone punctuation to previous word
words = []
for t in text:
    if re.fullmatch(r'[!?:;.,]+', t) and words:
        words[-1] += ' ' + t
    else:
        words.append(t)

def syl(w):
    w = w.lower()
    g = re.findall(r"[aeiouyàâäéèêëîïôöùûüœ]+", w)
    n = len(g)
    if w.rstrip('!?:;., ').endswith('e') and n > 1:
        n -= 0.6
    return max(0.6, n) + 0.25

wt = [syl(w) for w in words]
def btype(w):
    s = w.rstrip()
    if re.search(r'[.!?]$', s): return 'S'
    if re.search(r'[,:;]$', s): return 'W'
    return 'N'
bt = [btype(w) for w in words]  # boundary AFTER word i
N = len(words)
gaps = [tuple(map(float, l.split())) for l in open(W + '/gaps.txt')]
start_t = 0.0
if gaps and gaps[0][0] < 0.05:
    start_t = gaps[0][1]; gaps = gaps[1:]
DUR = float(sys.argv[2])
end_t = gaps[-1][0] if gaps[-1][1] > DUR - 0.3 else DUR
if gaps[-1][1] > DUR - 0.3: gaps = gaps[:-1]
G = len(gaps)
total_speech = (end_t - start_t) - sum(b - a for a, b in gaps)
rate = total_speech / sum(wt)
print('words', N, 'gaps', G, 'rate s/weight', round(rate, 3))
pre = [0.0]
for x in wt: pre.append(pre[-1] + x)
# cost of skipping boundary after word i (unmatched)
skipc = [{'S': 2.5, 'W': 0.4, 'N': 0.0}[b] for b in bt]
prs = [0.0]
for x in skipc: prs.append(prs[-1] + x)
matchc = {'S': 0.0, 'W': 0.3, 'N': 2.0}
# anchors: index -1 = start (boundary before word 0), gap j matched to boundary b (after word b)
INF = 1e18
# dp[j][b]
from collections import defaultdict
dp = {(-1, -1): 0.0}
back = {}
gend = lambda j: start_t if j == -1 else gaps[j][1]
def gcost(j):
    L = gaps[j][1] - gaps[j][0]
    return 1.0 + 4.0 * L
states_by_j = defaultdict(list); states_by_j[-1].append(-1)
for j in range(G):
    for b in range(0, N - 1):
        best = INF; arg = None
        for j0 in range(max(-1, j - 4), j):
            skipg = sum(gcost(k) for k in range(j0 + 1, j))
            for b0 in states_by_j[j0]:
                if b0 >= b or b - b0 > 70: continue
                c0 = dp[(j0, b0)]
                w = pre[b + 1] - pre[b0 + 1]
                dur = gaps[j][0] - gend(j0) - sum(gaps[k][1] - gaps[k][0] for k in range(j0 + 1, j))
                if dur <= 0.2: continue
                rc = 6.0 * abs(math.log(dur / (w * rate)))
                sb = prs[b] - prs[b0 + 1]
                c = c0 + rc + sb + skipg + matchc[bt[b]]
                if c < best: best = c; arg = (j0, b0)
        if arg is not None and best < 1e17:
            dp[(j, b)] = best; back[(j, b)] = arg; states_by_j[j].append(b)
    # prune
    lst = sorted(states_by_j[j], key=lambda b: dp[(j, b)])[:120]
    states_by_j[j] = lst
# final
best = INF; arg = None
for j0 in range(max(-1, G - 5), G):
    skipg = sum(gcost(k) for k in range(j0 + 1, G))
    for b0 in states_by_j[j0]:
        w = pre[N] - pre[b0 + 1]
        dur = end_t - gend(j0) - sum(gaps[k][1] - gaps[k][0] for k in range(j0 + 1, G))
        if dur <= 0.2: continue
        c = dp[(j0, b0)] + 6.0 * abs(math.log(dur / (w * rate))) + prs[N - 1] - prs[b0 + 1] + skipg
        if c < best: best = c; arg = (j0, b0)
path = []
cur = arg
while cur != (-1, -1):
    path.append(cur); cur = back[cur]
path.reverse()
anchors = [(-1, -1)] + path + [('END', N - 1)]
times = [None] * N
ends = [None] * N
for (ja, ba), (jb, bb) in zip(anchors, anchors[1:]):
    t0 = gend(ja)
    t1 = end_t if jb == 'END' else gaps[jb][0]
    w = pre[bb + 1] - pre[ba + 1]
    acc = 0.0
    for i in range(ba + 1, bb + 1):
        times[i] = t0 + (t1 - t0) * acc / w
        acc += wt[i]
        ends[i] = t0 + (t1 - t0) * acc / w
out = [{'w': words[i], 's': round(times[i], 3), 'e': round(ends[i], 3)} for i in range(N)]
json.dump(out, open(W + '/words.json', 'w'), ensure_ascii=False, indent=0)
print('cost', round(best, 2), 'matched', len(path))
for (j, b) in path:
    print(f"{gaps[j][0]:7.2f} | ...{' '.join(words[max(0,b-3):b+1])} || {' '.join(words[b+1:b+4])}")

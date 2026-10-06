import json,sys
S={n:json.load(open(f"{n}.json")) for n in ["mascots","behaviors","difficulty_scale","terminal_menu","game_hooks"]}
ids=lambda n:{r["id"] for r in S[n]["rows"]}
problems=[]
# unfilled cells (null) and unverified rows
for n,s in S.items():
    for r in s["rows"]:
        for c in s["columns"]:
            if c not in r: problems.append(f"{n}/{r.get('id',r.get('band'))}: missing column {c}")
            elif r[c] is None: problems.append(f"{n}/{r.get('id',r.get('band'))}: unfilled {c}")
        if r.get("verified") is False: problems.append(f"{n}/{r.get('id',r.get('band'))}: not verified in game")
# references
for r in S["mascots"]["rows"]:
    if r["behaviorId"] not in ids("behaviors"): problems.append(f"mascots/{r['id']}: unknown behavior {r['behaviorId']}")
for r in S["terminal_menu"]["rows"]:
    if r["mascotId"] and r["mascotId"] not in ids("mascots"): problems.append(f"terminal/{r['id']}: unknown mascot")
    if r["hookId"] and r["hookId"] not in ids("game_hooks"): problems.append(f"terminal/{r['id']}: unknown hook")
# coverage: every mascot has a slider; every behavior used
sliders={r["mascotId"] for r in S["terminal_menu"]["rows"] if r["mascotId"]}
for m in ids("mascots")-sliders: problems.append(f"mascots/{m}: no terminal slider")
for b in ids("behaviors")-{r["behaviorId"] for r in S["mascots"]["rows"]}: problems.append(f"behaviors/{b}: unused")
# difficulty bands cover 0-20 without gaps
lv=set()
for r in S["difficulty_scale"]["rows"]: lv|=set(range(r["minLevel"],r["maxLevel"]+1))
if lv!=set(range(21)): problems.append("difficulty_scale: bands do not cover 0-20")
refs=[p for p in problems if "unfilled" not in p and "not verified" not in p]
print(f"{len(problems)} open items ({len(refs)} broken references/coverage, rest unfilled or unverified)")
for p in problems: print(" -",p)
sys.exit(1 if problems else 0)

# engine.py  – full draft engine + one helper for Streamlit
# =========================================================

# ---------- Mappings (fixed for mirrored 3-v-3) ----------
mapping_A = {
    1: "A1", 4: "A2", 5: "A3",
    8: "A3", 9: "A2", 12: "A1",
    13: "A1", 16: "A2", 17: "A3",
    20: "A3", 21: "A2", 24: "A1"
}
mapping_B = {
    2: "B1", 3: "B2", 6: "B3",
    7: "B3", 10: "B2", 11: "B1",
    14: "B1", 15: "B2", 18: "B3",
    19: "B3", 22: "B2", 23: "B1"
}

# ---------- Node + generators ----------
class Node:
    def __init__(self, assigned_picks=None, a_possible=False, b_possible=False):
        self.assigned_picks = assigned_picks if assigned_picks else []
        self.a_possible = a_possible
        self.b_possible = b_possible

def calculate_free_combinations(assigned, team_order, opp_order,
                                 idx, total_free, base, out):
    if idx > total_free:
        out.append(assigned.copy())
        return
    current_move = team_order[idx-1]
    opp_count = sum(1 for m in opp_order if m < current_move)
    own_free  = idx-1
    max_pick  = opp_count + 1 + own_free + base
    start_val = assigned[-1] if assigned else base
    for v in range(start_val+1, max_pick+1):
        assigned.append(v)
        calculate_free_combinations(assigned, team_order, opp_order,
                                    idx+1, total_free, base, out)
        assigned.pop()

def calculate_team_with_locked(total_picks, team_order, opp_order,
                                locked_count, locked):
    locked_team = [locked[m-1] for m in team_order if m <= locked_count]
    free_cnt    = total_picks - len(locked_team)
    team_free   = [m-locked_count for m in team_order if m > locked_count]
    opp_free    = [m-locked_count for m in opp_order  if m > locked_count]
    base_val    = max(locked) if locked else 0
    free_res    = []
    calculate_free_combinations([], team_free, opp_free,
                                1, free_cnt, base_val, free_res)
    return [locked_team + lst for lst in free_res]

# ---------- helpers ----------
def filter_combinations(combos, included, excluded):
    inc = set(included) if included else set()
    exc = set(excluded) if excluded else set()
    out = []
    for c in combos:
        if inc and not inc.issubset(c):       continue
        if exc and exc.intersection(c):       continue
        out.append(c)
    return out

def group_by_prefix(combos, k):
    d = {}
    for c in combos:
        if len(c) < k: continue
        pre = tuple(c[:k])
        d[pre] = d.get(pre, 0) + 1
    return d

# ---------- one public function for Streamlit ----------
def run_analysis(total_picks, role, locked, included, excluded, prefix_len):
    """
    Returns header string and list[dict] rows for UI.
    """
    A_order = [1,4,5,8,9,12,13,16,17,20,21,24][:total_picks]
    B_order = [2,3,6,7,10,11,14,15,18,19,22,23][:total_picks]

    combos = calculate_team_with_locked(
        total_picks,
        A_order if role=="A" else B_order,
        B_order if role=="A" else A_order,
        len(locked),
        locked
    )
    combos = filter_combinations(combos, included, excluded)
    groups = group_by_prefix(combos, prefix_len)

    mapping    = mapping_A if role=="A" else mapping_B
    move_order = A_order   if role=="A" else B_order
    rows = []
    for pre, cnt in sorted(groups.items()):
        move = move_order[prefix_len-1]
        rows.append({
            "Prefix":   pre,
            "Count":    cnt,
            "Percent":  f"{cnt/len(combos)*100:.1f}",
            "Move":     move,
            "Player":   mapping.get(move, "?")
        })
    header = f"{len(combos)} valid combinations after filters"
    return header, rows

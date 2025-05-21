# engine.py  (bottom of file)
# ------------------------------------------------------------
def run_analysis(total_picks,            # 9 or 12
                 role,                   # "A" or "B"
                 locked,                 # list[int]
                 included, excluded,     # list[int]
                 prefix_len):
    """
    Return header string + list[dict] suitable for a Streamlit table.
    """
    teamA_order = [1,4,5,8,9,12,13,16,17,20,21,24][:total_picks]
    teamB_order = [2,3,6,7,10,11,14,15,18,19,22,23][:total_picks]

    combos = calculate_team_with_locked(
        total_picks,
        teamA_order if role=="A" else teamB_order,
        teamB_order if role=="A" else teamA_order,
        len(locked),
        locked
    )
    combos = filter_combinations(combos, included, excluded)
    groups = group_by_prefix(combos, prefix_len)

    mapping = mapping_A if role=="A" else mapping_B
    move_order = teamA_order if role=="A" else teamB_order

    rows = []
    for prefix, cnt in sorted(groups.items()):
        move = move_order[prefix_len-1]
        rows.append({
            "Prefix": prefix,
            "Count":  cnt,
            "Percent": f"{cnt/len(combos)*100:.1f}",
            "Move":   move,
            "Player": mapping.get(move, "?")
        })
    header = f"{len(combos)} valid combinations after filters"
    return header, rows

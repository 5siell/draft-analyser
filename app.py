import streamlit as st
import pandas as pd
from engine import run_analysis

st.set_page_config(page_title="3v3 Draft Explorer", layout="wide")
st.title("Warzone 3v3 Mirror-Draft Explorer")

# ---------- sidebar inputs ----------
with st.sidebar:
    st.header("Parameters")
    total_picks = st.selectbox("Picks per team", [9, 12], index=1)
    role        = st.radio("Assume we are", ["A", "B"])
    locked_txt  = st.text_input("Locked picks (comma-sep)", "1,2,3")
    inc_txt     = st.text_input("Included / ours", "")
    exc_txt     = st.text_input("Excluded / lost", "")
    prefix_len  = st.slider("Prefix length", 2, total_picks, 6)

def to_list(txt):
    return [int(x) for x in txt.split(",") if x.strip().isdigit()]

locked   = to_list(locked_txt)
included = to_list(inc_txt)
excluded = to_list(exc_txt)

# ---------- run engine ----------
header, rows = run_analysis(total_picks, role, locked, included, excluded, prefix_len)

st.markdown(f"### {header}")
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No combinations with these filters.")

import streamlit as st
import pandas as pd
from engine import run_analysis

st.set_page_config(page_title="3v3 Draft Explorer", layout="wide")
st.title("Warzone 3v3 Mirror-Draft Explorer")

# ---------- sidebar ----------
with st.sidebar:
    st.header("Parameters")
    picks = st.selectbox("Picks per team", [9, 12], index=1)
    role  = st.radio("Assume we are", ["A", "B"])
    locked_txt  = st.text_input("Locked picks (comma-sep)", "1,2")
    inc_txt     = st.text_input("Included / ours", "")
    exc_txt     = st.text_input("Excluded / lost", "")
    k           = st.slider("Prefix length", 2, picks, 6)

def to_int_list(txt):
    return [int(x) for x in txt.split(",") if x.strip().isdigit()]

locked   = to_int_list(locked_txt)
included = to_int_list(inc_txt)
excluded = to_int_list(exc_txt)

# ---------- run engine ----------
header, rows = run_analysis(picks, role, locked, included, excluded, k)

st.markdown(f"### {header}")
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.warning("No combinations with these settings.")

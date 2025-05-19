import streamlit as st

from state import init_state

st.set_page_config(page_title="HexaPawn", initial_sidebar_state="collapsed")
init_state()
st.switch_page("pages/config.py")

import streamlit as st


def change_page():
    st.session_state.jump_to_main = True


st.markdown("# HexaPawn Configuration")
st.markdown(
    """
    ## Game Rules
    - Players take turns moving their pawns.
    - Pawns can move forward one square or capture diagonally.
    - The game ends when one player captures all the opponent's pawns or blocks them.
    """
)
st.number_input(
    "Number of Pawns", min_value=3, max_value=10, value="min", key="_num_pawns"
)
st.selectbox("First turn", options=["Player", "AI"], key="_first_turn")
st.selectbox("AI Type", options=["Pure", "Adaptive"], key="_ai_type")
st.button("Start Game", on_click=change_page)

if st.session_state.get("jump_to_main", False):
    st.session_state.jump_to_main = False
    st.session_state.reset_game = True
    st.session_state.num_pawns = st.session_state.get("_num_pawns", 3)
    st.session_state.first_turn = st.session_state.get("_first_turn", "Player")
    st.session_state.ai_type = st.session_state.get("_ai_type", "minimax").lower()
    st.switch_page("pages/main.py")

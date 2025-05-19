import streamlit as st


def init_state():
    defaults = {
        "num_pawns": 3,
        "first_turn": "Player",
        "board": [["C"] * 3] + [["."] * 3 for _ in range(1)] + [["P"] * 3],
        "selected": None,
        "turn": "P",
        "turn_count": 0,
        "reset_game": False,
        "jump_to_config": False,
        "jump_to_main": False,
        "ai_type": "minimax",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

import time

import streamlit as st

import minimax_ai_adaptive
import minimax_ai_pure
from game_logic import check_winner

# Emojis for players
PLAYER_ICON = "👤"
COMPUTER_ICON = "🤖"
EMPTY_ICON = ""


def get_icon(symbol):
    return {"P": "👤", "C": "🤖", ".": "\u00a0" * 6}.get(  # space char for button size
        symbol, "\u00a0" * 6
    )


def display_board():
    board = st.session_state.board
    for i, row in enumerate(board):
        cols = st.columns(st.session_state.num_pawns)
        for j, cell in enumerate(row):
            icon = get_icon(cell)
            button_color = "#f0d9b5" if (i + j) % 2 == 0 else "#b58863"
            button_key = f"cell_{i}_{j}"

            custom_css = f"""
            <style>
            div[data-testid="stButton"][key="{button_key}"] > button {{
                height: 100px;
                width: 100px;
                font-size: 30px;
                background-color: {button_color};
                border: 1px solid #444;
                border-radius: 6px;
                padding: 0;
            }}
            </style>
            """

            cols[j].markdown(custom_css, unsafe_allow_html=True)
            if cols[j].button(icon, key=button_key):
                handle_click(i, j)


def handle_click(i, j):
    board = st.session_state.board
    current = st.session_state.turn
    selected = st.session_state.selected

    if selected:
        si, sj = selected
        direction = -1 if current == "P" else 1
        opponent = "C" if current == "P" else "P"

        # Forward move
        if i == si + direction and j == sj and board[i][j] == ".":
            board[i][j] = board[si][sj]
            board[si][sj] = "."
            st.session_state.turn = "C" if current == "P" else "P"
            st.session_state.turn_count += 1
            st.session_state.selected = None
            st.rerun()
            return

        # Diagonal capture
        if i == si + direction and abs(j - sj) == 1 and board[i][j] == opponent:
            board[i][j] = board[si][sj]
            board[si][sj] = "."
            st.session_state.turn = "C" if current == "P" else "P"
            st.session_state.turn_count += 1
            st.session_state.selected = None
            st.rerun()
            return

        # Invalid move
        st.session_state.selected = None
        st.rerun()
    else:
        if board[i][j] == current:
            st.session_state.selected = (i, j)
            st.rerun()


def reset_game():
    size = st.session_state.num_pawns
    first = st.session_state.first_turn
    st.session_state.board = (
        [["C"] * size] + [["."] * size for _ in range(size - 2)] + [["P"] * size]
    )
    st.session_state.selected = None
    st.session_state.turn = "P" if first == "Player" else "C"
    st.session_state.turn_count = 0
    st.session_state.ai_type = st.session_state.get("ai_type", "minimax")
    if st.session_state.get("reset_game", False):
        st.session_state.reset_game = False
        st.rerun()


def change_page():
    st.session_state.jump_to_config = True


# Select AI based on session state
ai_type = st.session_state.get("ai_type", "minimax")
if ai_type == "adaptive":
    get_best_move = minimax_ai_adaptive.get_best_move
    make_move = minimax_ai_adaptive.make_move
else:
    get_best_move = minimax_ai_pure.get_best_move
    make_move = minimax_ai_pure.make_move


# check for reset
if st.session_state.reset_game:
    reset_game()

# check for winner
winner = check_winner(st.session_state.board, st.session_state.turn)
if winner:
    st.success(
        f"🎉 {'Player 👤' if winner == 'P' else 'AI 🤖'} wins after {st.session_state.turn_count} truns!"
    )
    st.button("🔁 Play Again", on_click=change_page)


# Display
st.markdown("# HexaPawn")
display_board()
st.markdown(
    f"**Current turn:** {'Player 👤' if st.session_state.turn == 'P' else 'AI 🤖'}"
)
st.button("🔁 Reset Game", on_click=reset_game)


# move AI
if st.session_state.turn == "C" and not winner:
    st.session_state.selected = None
    time.sleep(0.5)
    best_pawn, best_move = get_best_move(st.session_state.board)
    st.session_state.board = make_move(
        st.session_state.board, best_pawn[0], best_pawn[1], best_move[0], best_move[1]
    )
    st.session_state.turn = "P"
    st.session_state.turn_count += 1
    st.rerun()


# check for page change
if st.session_state.get("jump_to_config", False):
    st.session_state.jump_to_config = False
    st.switch_page("pages/config.py")

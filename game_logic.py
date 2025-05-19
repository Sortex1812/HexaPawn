def check_winner(board, current_turn) -> str | None:
    # Pawn reached end?
    if "P" in board[0]:
        return "P"
    if "C" in board[-1]:
        return "C"

    # All pawns captured?
    has_p = any("P" in row for row in board)
    has_e = any("C" in row for row in board)
    if not has_p:
        return "C"
    if not has_e:
        return "P"

    # Player has no more moves
    if not has_legal_moves(board, current_turn):
        return "C" if current_turn == "P" else "P"

    return None


def has_legal_moves(board, player) -> bool:
    direction = -1 if player == "P" else 1
    opponent = "C" if player == "P" else "P"
    size = len(board)

    for i in range(size):
        for j in range(size):
            if board[i][j] != player:
                continue
            ni = i + direction

            if ni in range(size):
                # Forward move
                if board[ni][j] == ".":
                    return True
                # Diagonal captures
                for dj in [-1, 1]:
                    nj = j + dj
                    if nj in range(size) and board[ni][nj] == opponent:
                        return True
    return False

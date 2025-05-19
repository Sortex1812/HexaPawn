from game_logic import check_winner


def get_best_move(board) -> tuple[list[int], list[int]]:
    best_pawn = [0, 0]
    best_move = [0, 0]
    best_value = float("-inf")
    size = len(board)

    # average distance between P and C in each column
    distances = []
    for col in range(size):
        p_rows = [row for row in range(size) if board[row][col] == "P"]
        c_rows = [row for row in range(size) if board[row][col] == "C"]
        if p_rows and c_rows:
            # Both players present: normal distance
            distance = max(p_rows) - min(c_rows) - 1
            if distance >= 0:
                distances.append(distance)
        elif p_rows:
            # Only P present: treat as strong advantage for P (very small distance)
            distances.append(-5)
        elif c_rows:
            # Only C present: strong advantage for C (very small distance)
            distances.append(5)
    avg_distance = sum(distances) / len(distances) if distances else size

    # Count pawns
    p_count = sum(cell == "P" for row in board for cell in row)
    c_count = sum(cell == "C" for row in board for cell in row)

    # Adaptive depth
    depth = max(3, min(10, int(size + 4 - avg_distance - 0.5 * abs(p_count - c_count))))

    for i in range(size):
        for j in range(size):
            if board[i][j] == "C":
                for move in get_possible_moves(board, i, j):
                    new_board = make_move(board, i, j, move[0], move[1])
                    board_value = minimax(new_board, depth, False, 0)
                    if board_value > best_value:
                        best_value = board_value
                        best_move = move
                        best_pawn = [i, j]
    print(f"Best move for C: {best_move} from {best_pawn}")
    return best_pawn, best_move


def minimax(board, depth, is_maximizing, turn) -> float:
    size = len(board)
    winner = check_winner(board, "C" if is_maximizing else "P")
    if winner == "C":
        return 100
    elif winner == "P":
        return -100

    if depth == 0:
        return evaluate_board(board) - turn

    if is_maximizing:
        best_value = float("-inf")
        for i in range(size):
            for j in range(size):
                if board[i][j] == "C":
                    for move in get_possible_moves(board, i, j):
                        new_board = make_move(board, i, j, move[0], move[1])
                        best_value = max(
                            best_value, minimax(new_board, depth - 1, False, turn + 1)
                        )
        return best_value
    else:
        best_value = float("inf")
        for i in range(size):
            for j in range(size):
                if board[i][j] == "P":
                    for move in get_possible_moves(board, i, j):
                        new_board = make_move(board, i, j, move[0], move[1])
                        best_value = min(
                            best_value, minimax(new_board, depth - 1, True, turn + 1)
                        )
        return best_value


def get_possible_moves(board, i, j) -> list[list[int]]:
    size = len(board)
    moves = []
    direction = -1 if board[i][j] == "P" else 1
    opponent = "C" if board[i][j] == "P" else "P"

    # forward
    ni = i + direction
    if ni in range(size) and board[ni][j] == ".":
        moves.append([ni, j])

    # captures
    for dj in [-1, 1]:
        nj = j + dj
        if ni in range(size) and nj in range(size) and board[ni][nj] == opponent:
            moves.append([ni, nj])

    return moves


def make_move(board, i, j, ni, nj) -> list[list[str]]:
    new_board = [row[:] for row in board]
    new_board[ni][nj] = new_board[i][j]
    new_board[i][j] = "."
    return new_board


def evaluate_board(board) -> float:
    size = len(board)
    p_score = sum(cell == "P" for row in board for cell in row)
    c_score = sum(cell == "C" for row in board for cell in row)

    # winning columns
    for col in range(size):
        if board[0][col] == "P":
            p_score += float("inf")
        elif board[-1][col] == "C":
            c_score += float("inf")

    # columns with only one player's pawns
    for col in range(size):
        p_in_col = any(board[row][col] == "P" for row in range(size))
        c_in_col = any(board[row][col] == "C" for row in range(size))
        if p_in_col and not c_in_col:
            p_score += 3
        elif c_in_col and not p_in_col:
            c_score += 3

    # advancement and capture opportunities
    for i in range(size):
        for j in range(size):
            cell = board[i][j]
            if cell == "P":
                # Advancement
                p_score += size - i
                # Capture opportunities
                for dj in [-1, 1]:
                    ni, nj = i - 1, j + dj
                    if 0 <= ni < size and 0 <= nj < size and board[ni][nj] == "C":
                        p_score += 2
            elif cell == "C":
                # Advancement
                c_score += i + 1
                # Capture opportunities
                for dj in [-1, 1]:
                    ni, nj = i + 1, j + dj
                    if 0 <= ni < size and 0 <= nj < size and board[ni][nj] == "P":
                        c_score += 2

    return p_score - c_score

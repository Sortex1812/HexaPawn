from game_logic import check_winner

def get_best_move(board) -> tuple[list[int], list[int]]:
    best_pawn = [0, 0]
    best_move = [0, 0]
    best_value = float('-inf')
    size = len(board)

    for i in range(size):
        for j in range(size):
            if board[i][j] == "C":
                for move in get_possible_moves(board, i, j):
                    new_board = make_move(board, i, j, move[0], move[1])
                    board_value = minimax(new_board, 5, False)
                    if board_value > best_value:
                        best_value = board_value
                        best_move = move
                        best_pawn = [i, j]
    print(f"Best move for C: {best_move} from {best_pawn}")
    return best_pawn, best_move

def minimax(board, depth, is_maximizing) -> float:
    size = len(board)
    winner = check_winner(board, "C" if is_maximizing else "P")
    if winner == "C":
        return 100
    elif winner == "P":
        return -100

    if depth == 0:
        return evaluate_board(board)

    if is_maximizing:
        best_value = float('-inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "C":
                    for move in get_possible_moves(board, i, j):
                        new_board = make_move(board, i, j, move[0], move[1])
                        best_value = max(best_value, minimax(new_board, depth - 1, False))
        return best_value
    else:
        best_value = float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "P":
                    for move in get_possible_moves(board, i, j):
                        new_board = make_move(board, i, j, move[0], move[1])
                        best_value = min(best_value, minimax(new_board, depth - 1, True))
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

def evaluate_board(board) -> int:
    p_count = sum(row.count("P") for row in board)
    c_count = sum(row.count("C") for row in board)
    if 'C' in board[0]:
        c_count += 10
    if 'P' in board[-1]:
        p_count += 10
    return p_count - c_count
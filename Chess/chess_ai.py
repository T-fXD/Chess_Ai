import chess
import chess.pgn

rows = chess.RANK_NAMES
cols = chess.FILE_NAMES

p = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [7, 7, 7, 7, 7, 7, 7, 7],
     [5, 5, 5, 6, 6, 5, 5, 5],
     [0, 0, 3, 4, 4, 3, 0, 0],
     [0, 0, 5, 6, 6, 5, 0, 0],
     [0, 2, 3, 4, 4, 3, 2, 0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

k = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [2, 3, 3, 3, 3, 3, 3, 2],
     [1, 2, 2, 2, 2, 2, 2, 1],
     [0, 1, 1, 1, 1, 1, 1, 0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [1, 1, 1, 0, 0, 1, 1, 1],
     [2, 3, 3, 0, 0, 2, 3, 2]]

r = [[0, 1, 2, 4, 4, 2, 1, 0],
     [0, 0, 1, 3, 3, 1, 0, 0],
     [0, 0, 0, 2, 2, 0, 0, 0],
     [0, 0, 0, 2, 2, 0, 0, 0],
     [0, 0, 0, 2, 2, 0, 0, 0],
     [0, 0, 1, 3, 3, 1, 0, 0],
     [0, 1, 2, 4, 4, 2, 1, 0],
     [1, 2, 3, 5, 5, 3, 2, 1]]

n = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0, 3, 4, 4, 4, 4, 3, 0],
     [0, 0, 4, 4, 4, 4, 0, 0],
     [0, 0, 3, 4, 4, 3, 0, 0],
     [0, 0, 3, 3, 3, 3, 0, 0],
     [0, 0, 1, 2, 2, 1, 0, 0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

b = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
     [0, 3, 1, 1, 1, 1, 3, 0],
     [0, 0, 3, 4, 4, 3, 0, 0],
     [0, 0, 4, 2, 2, 4, 0, 0],
     [0, 4, 1, 2, 2, 1, 4, 0],
     [3, 0, 0, 0, 0, 0, 0, 3]]

def evaluate_board(board, ai):
    score = 0

    for row in range(8):
        for col in range(8):
            square_index = row * 8 + col
            square = chess.SQUARES[square_index]
            piece = board.piece_at(square)

            if piece != None:
                piece_symbol = piece.symbol()

                if ai == "b":
                    if piece_symbol == "P":
                        score -= 10
                    if piece_symbol == "N":
                        score -= 30
                    if piece_symbol == "B":
                        score -= 30
                    if piece_symbol == "R":
                        score -= 50
                    if piece_symbol == "Q":
                        score -= 90

                    if piece_symbol == "p":
                        score += 10
                        score += p[row][col]
                    if piece_symbol == "n":
                        score += 30
                        score += n[row][col]
                    if piece_symbol == "b":
                        score += 30
                        score += b[row][col]
                    if piece_symbol == "r":
                        score += 50
                        score += r[row][col]
                    if piece_symbol == "q":
                        score += 90
                        score += ((b[row][col] + r[row][col]) / 2)
                    if piece_symbol == "k":
                        score += k[row][col]

                else:
                    if piece_symbol == "P":
                        score += 10
                        score += p[-row + col][col]
                    if piece_symbol == "N":
                        score += 30
                        score += n[-row + col][col]
                    if piece_symbol == "B":
                        score += 30
                        score += b[-row + col][col]
                    if piece_symbol == "R":
                        score += 50
                        score += r[-row + col][col]
                    if piece_symbol == "Q":
                        score += 90
                        score += ((r[-row + col][col] + b[-row + col][col]) / 2)
                    if piece_symbol == "K":
                        score += k[-row + col][col]

                    if piece_symbol == "p":
                        score -= 10
                    if piece_symbol == "n":
                        score -= 30
                    if piece_symbol == "b":
                        score -= 30
                    if piece_symbol == "r":
                        score -= 50
                    if piece_symbol == "q":
                        score -= 90

    for move in board.legal_moves:
        score += 0.1

    return score

def minimax(board, max_depth, ai):
    """
    Returns the optimal action for the current player on the board.
    """

    def alg(board, depth, ismax):
        """
        The actual minimax algorithm
        """

        score = 0

        if board.is_variant_end():
            if board.is_variant_draw():
                return 0
            if board.is_variant_win():
                return 100000
            if board.is_variant_loss():
                return -100000

        if depth >= max_depth:
            score = evaluate_board(board, ai)
            return score

        if ismax:
            bestScore = -1000000
            for move in board.legal_moves:
                move = (board.san(move))
                board.push_san(move)
                score = alg(board, depth + 1, False)
                board.pop()
                if score > bestScore:
                    bestScore = score

            return bestScore

        else:
            bestScore = 1000000
            for move in board.legal_moves:
                move = (board.san(move))
                board.push_san(move)
                score = alg(board, depth + 1, True)
                board.pop()
                if score < bestScore:
                    bestScore = score

            return bestScore

    bestScore = -1000000
    for move in board.legal_moves:
        str(move)
        move = (board.san(move))
        board.push_san(move)
        score = alg(board, 1, False)
        board.pop()
        if score > bestScore:
            bestScore = score
            bestMove = move

    try:
        print(bestScore)
        return bestMove
    except:
        quit("Game Over")
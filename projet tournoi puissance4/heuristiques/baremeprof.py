def heuristique(board, player):
    # Fonction heuristique 2 qui privilégie les cases centrales
    position_scores = [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ]

    score = 0
    for row in range(6):
        for col in range(7):
            if board[row][col] == player:
                score += position_scores[row][col]
            elif board[row][col] != ' ':
                score -= position_scores[row][col]

    return score
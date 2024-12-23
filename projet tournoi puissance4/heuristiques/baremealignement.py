def heuristique(board, player):

    def heuristique1(board, player):
        def evaluate_segment(board, start_row, start_col, delta_row, delta_col, player):
            score = 0
            opponent = 'O' if player == 'X' else 'X'
            player_count = 0
            opponent_count = 0
            empty_count = 0

            for i in range(4):
                cell = board[start_row + i * delta_row][start_col + i * delta_col]
                if cell == player:
                    player_count += 1
                elif cell == opponent:
                    opponent_count += 1
                else:
                    empty_count += 1

            if player_count == 4:
                score += 100000
            elif player_count == 3 and empty_count == 1:
                score += 100
            elif player_count == 2 and empty_count == 2:
                score += 10
            elif player_count == 1 and empty_count == 3:
                score += 1

            if opponent_count == 4:
                score -= 100000
            elif opponent_count == 3 and empty_count == 1:
                score -= 100
            elif opponent_count == 2 and empty_count == 2:
                score -= 10
            elif opponent_count == 1 and empty_count == 3:
                score -= 1

            return score

        # Fonction heuristique initiale
        score = 0

        # Vérifier les lignes horizontales
        for row in range(6):
            for col in range(4):
                score += evaluate_segment(board, row, col, 0, 1, player)

        # Vérifier les lignes verticales
        for row in range(3):
            for col in range(7):
                score += evaluate_segment(board, row, col, 1, 0, player)

        # Vérifier les diagonales montantes
        for row in range(3):
            for col in range(4):
                score += evaluate_segment(board, row, col, 1, 1, player)

        # Vérifier les diagonales descendantes
        for row in range(3, 6):
            for col in range(4):
                score += evaluate_segment(board, row, col, -1, 1, player)

        return score



    position_scores = [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ]

    segment_score = heuristique1(board, player)
    position_score = 0

    for row in range(6):
        for col in range(7):
            if board[row][col] == player:
                position_score += position_scores[row][col]
            elif board[row][col] != ' ':
                position_score -= position_scores[row][col]

    return segment_score + position_score
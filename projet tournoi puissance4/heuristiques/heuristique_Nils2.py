def heuristique(board,player):
    def heuristique_position(board, player):
        position_scores = [
            [3, 4, 5, 7, 5, 4, 3],
            [4, 6, 8, 10, 8, 6, 4],
            [5, 6, 8, 8, 8, 6, 5],
            [5, 6, 8, 8, 8, 6, 5],
            [4, 6,10, 12, 10, 6, 4],
            [3, 5, 10, 15, 10, 5, 3]
            ]
        score = 0
        for row in range(6):
            for col in range(7):
                if board[row][col] == player:
                    score += position_scores[row][col]
                elif board[row][col] != ' ':
                    score -= position_scores[row][col]

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
            score += 50
        elif player_count == 3 and empty_count == 1:
            score += 20
        elif player_count == 2 and empty_count == 2:
            score += 10
        elif player_count == 1 and empty_count == 3:
            score += 1

        if opponent_count == 4:
            score -= 50
        elif opponent_count == 3 and empty_count == 1:
            score -= 20
        elif opponent_count == 2 and empty_count == 2:
            score -= 10
        elif opponent_count == 1 and empty_count == 3:
            score -= 1

        return score

    def heuristique_alignement(board, player):
        score = 0
        for row in range(6):
            for col in range(4):
                score += evaluate_segment(board, row, col, 0, 1, player)
        for row in range(3):
            for col in range(7):
                score += evaluate_segment(board, row, col, 1, 0, player)
        for row in range(3):
            for col in range(4):
                score += evaluate_segment(board, row, col, 1, 1, player)
        for row in range(3, 6):
            for col in range(4):
                score += evaluate_segment(board, row, col, -1, 1, player)
        return score

    score=0
    opponent='O' if player=='X' else 'X'
    compteur=0
    for row in range(6):
        for col in range(7):
            if  board[row][col]!= '':
                compteur += 1
            else:
                compteur +=0
    if compteur<=5:
        heuristique_position(board,player)
    else :
        heuristique_alignement(board,player)
    return score 

    




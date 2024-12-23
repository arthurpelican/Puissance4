def heuristique(board, player):
    def eval_segment(board, start_row, start_col, delta_row, delta_col, player):
        score = 0
        opponent = 'O' if player == 'X' else 'X'
        segment = []
        for i in range(4):
            segment.append(board[start_row + i * delta_row][start_col + i * delta_col])

        if segment == [player,player,player,player]:
            score += 10000  #victoire !
        elif segment == [opponent,opponent,opponent,opponent]:
            score -= 10000  #défaite
        for i in range(0,2):
            a = segment[i]
            b = segment[i+1]
            c = segment[i+2]
            if ['',player,player] in [[a,b,c],[a,c,b],[c,a,b]]:
                score += 20# OO_ et permutations
            elif [player,player,player] == [a,b,c]:
                score += 50 # OOO
            elif [player,player,opponent] in [[a,b,c],[c,a,b]]:
                score += 10 # XOO ou OOX
            elif ['',opponent,opponent] in [[a,b,c],[a,c,b],[c,a,b]]:
                score += -20 # XX_ et permutations
            elif [opponent,opponent,opponent] == [a,b,c]:
                score += -50 # XXX
            elif [opponent,opponent,player] in [[a,b,c],[c,a,b]]:
                score += -10 # OXX ou XOO
        return score

    position_scores = [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ]
    score = 0
    for row in range(6): # Vérifier les lignes horizontales
        for col in range(4):
            score += eval_segment(board, row, col, 0, 1, player)

    for row in range(3):  # Vérifier les lignes verticales
        for col in range(7):
            score += eval_segment(board, row, col, 1, 0, player)

    for row in range(3):   # Vérifier les diagonales montantes
        for col in range(4):
            score += eval_segment(board, row, col, 1, 1, player)

    for row in range(3, 6): # Vérifier les diagonales descendantes
        for col in range(4):
            score += eval_segment(board, row, col, -1, 1, player)


    position_score = 0

    for row in range(6):
        for col in range(7):
            if board[row][col] == player:
                position_score += position_scores[row][col]
            elif board[row][col] != ' ':
                position_score -= position_scores[row][col]

    return score+position_score

def heuristique(board,player):
    def evaluate_line(cell1, cell2, cell3, player):
        score = 0

        opponent = 'O' if player == 'X' else 'X'

        # Premier cas : toutes les cellules sont du joueur
        if cell1 == cell2 == cell3 == player:
            score = 1000
        # Deuxième cas : deux cellules sont du joueur et une est vide
        elif cell1 == cell2 == player and cell3 == ' ':
            score = 10
        elif cell1 == cell3 == player and cell2 == ' ':
            score = 10
        elif cell2 == cell3 == player and cell1 == ' ':
            score = 10
        # Troisième cas : une cellule est du joueur et les autres sont vides
        elif cell1 == player and cell2 == cell3 == ' ':
            score = 1
        elif cell2 == player and cell1 == cell3 == ' ':
            score = 1
        elif cell3 == player and cell1 == cell2 == ' ':
            score = 1

        # Déduire les points si l'adversaire est en position similaire
        if cell1 == cell2 == cell3 == opponent:
            score = -1000
        elif cell1 == cell2 == opponent and cell3 == ' ':
            score = -10
        elif cell1 == cell3 == opponent and cell2 == ' ':
            score = -10
        elif cell2 == cell3 == opponent and cell1 == ' ':
            score = -10
        elif cell1 == opponent and cell2 == cell3 == ' ':
            score = -1
        elif cell2 == opponent and cell1 == cell3 == ' ':
            score = -1
        elif cell3 == opponent and cell1 == cell2 == ' ':
            score = -1

        return score

    valeurs = [
        [1, 0, 1],
        [0, 2, 0],
        [1, 0, 1]
    ]

    score1 = 0
    opponent = 'O' if player == 'X' else 'X'

    for row in range(3):
        for col in range(3):
            if board[row][col] == player:
                score1 += valeurs[row][col]
            elif board[row][col] == opponent:
                score1 -= valeurs[row][col]

    score2 = 0

    # Vérifier les lignes
    for row in range(3):
        score2 += evaluate_line(board[row][0], board[row][1], board[row][2], player)

    # Vérifier les colonnes
    for col in range(3):
        score2 += evaluate_line(board[0][col], board[1][col], board[2][col], player)

    # Vérifier les diagonales
    score2 += evaluate_line(board[0][0], board[1][1], board[2][2], player)
    score2 += evaluate_line(board[0][2], board[1][1], board[2][0], player)

    return max(score1,score2)
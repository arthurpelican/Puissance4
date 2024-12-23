def afficher_plateau(board,avec_pause=False):
    for row in board:
        print('  ' + ' | '.join(row))
        print('  ' + '-' * 29)
    if avec_pause:
        input('press to continue')

def check_win(board, player):
    # Vérifier les lignes horizontales
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vérifier les lignes verticales
    for row in range(3):
        for col in range(7):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Vérifier les diagonales montantes
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Vérifier les diagonales descendantes
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

def trouver_ligne_libre(board, col):
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def minimax(board, depth, maximizingPlayer, player, heuristique_fn):
    # Déterminer l'adversaire
    opponent = 'O' if player == 'X' else 'X'

    # Condition d'arrêt : profondeur atteinte ou fin de partie
    if depth == 0 or check_win(board, player) or check_win(board, opponent) or not any(' ' in row for row in board):
        return heuristique_fn(board, player)

    if maximizingPlayer:
        # Maximizing player (joueur actif)
        maxEval = -float('inf')
        for col in range(7):
            row = trouver_ligne_libre(board, col)
            if row is not None:  # Si on peut jouer dans cette colonne
                board[row][col] = player  # Simuler le coup
                eval = minimax(board, depth - 1, False, player, heuristique_fn)  # Récursion
                board[row][col] = ' '  # Annuler le coup
                maxEval = max(maxEval, eval)  # Garder le meilleur score
        return maxEval
    else:
        # Minimizing player (adversaire)
        minEval = float('inf')
        for col in range(7):
            row = trouver_ligne_libre(board, col)
            if row is not None:  # Si on peut jouer dans cette colonne
                board[row][col] = opponent  # Simuler le coup
                eval = minimax(board, depth - 1, True, player, heuristique_fn)  # Récursion
                board[row][col] = ' '  # Annuler le coup
                minEval = min(minEval, eval)  # Garder le pire score
        return minEval

def meilleur_coup(board, player, heuristique_fn):
    best_score = -float('inf')
    best_move = None

    for col in range(7):
        row = trouver_ligne_libre(board, col)
        if row is not None:
            board[row][col] = player
            score = minimax(board, 2 , False, player, heuristique_fn)
            board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_move = col

    return best_move

def jouer_match(dico, heuristiqueX, heuristiqueO,result,afficher = False):
    board = [[' ' for _ in range(7)] for _ in range(6)]
    current_player = 'X'
    heuristiques = [dico[heuristiqueX], dico[heuristiqueO]]

    for _ in range(42):  # Il y a au plus 42 coups dans une partie de Puissance 4
        move = meilleur_coup(board, current_player, heuristiques[0])
        if move is not None:
            row = trouver_ligne_libre(board, move)

            board[row][move] = current_player

            if afficher :
                afficher_plateau(board)
                print("\n")

            if check_win(board, current_player):
                if current_player == "O" :
                    result.put(heuristiqueO)
                    return
                else :
                    result.put(heuristiqueX)
                    return

            current_player = 'O' if current_player == 'X' else 'X'
            heuristiques.reverse()  # Alterner entre heuristique1 et heuristique2
        else:
            return
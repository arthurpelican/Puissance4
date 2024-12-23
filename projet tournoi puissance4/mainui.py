import os
import codeprof as game
import multiprocessing as mp
import pygame
import random as rd
import time

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duels d'heuristiques au Puissance 4")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (245, 200, 0)
DARK_YELLOW = (205, 160, 0)
RED = (245, 70, 39)
DARK_RED = (205, 30, 0)
BLUE = (49, 39, 245)
DARK_BLUE = (9, 0, 205)
GREEN = (77, 245, 39)
DARK_GREEN = (37, 205, 0)
GREY1 = (200, 200, 200)
GREY2 = (160, 160, 160)
VIOLET = (210, 107, 222)
DARK_VIOLET = (134, 22, 222)

font = "garamond"

MAIN_FONT = pygame.font.SysFont(font, 50)
LITTLE_FONT = pygame.font.SysFont(font, 30)
END_FONT = pygame.font.SysFont(font, 200)
MENU_FONT = pygame.font.SysFont(font, 100)

def draw_game(win, board, h1, h2, item, column, hidenext = False) :
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

    # Dessin du plateau
    pygame.draw.rect(win, GREY2, (65, 245, 840, 720))
    pygame.draw.rect(win, GREY1, (80, 260, 840, 720))

    # Selection de colonne
    for i in range(7) :
        if column == i :
            pygame.draw.rect(win, DARK_GREEN, (80 + 120*i, 260, 120, 720))

    for ligne in range(6) :
        for colonne in range(7) :
            if board[ligne][colonne] == " " :
                color = WHITE
            elif board[ligne][colonne] == "X" : 
                color = RED
            else :
                color = YELLOW
            
            pygame.draw.circle(win, color, (140 + colonne * 120, 320 + ligne * 120), 50)

    # taille des cases : 120 (bordure = 10)
    # taille de la grille : 720 * 840

    # Affichage de heuristique1 VS heuristique2
    text1 = MAIN_FONT.render(h1, 1, RED)
    text2 = MAIN_FONT.render("VS", 1, BLUE)
    text3 = MAIN_FONT.render(h2, 1, YELLOW)

    win.blit(text1, (20, 20))
    win.blit(text2, ((WIDTH - text2.get_width())//2, 20))
    win.blit(text3, (WIDTH - 20 - min(340, text3.get_width()), 20))

    # Affichage des boutons : Prochain coup, aller a la fin, quitter

    if not hidenext :
        if item == 0 :
            pygame.draw.rect(win, GREEN, (65, 85, 130, 130))
        else :
            pygame.draw.rect(win, DARK_BLUE, (65, 85, 130, 130))
        pygame.draw.rect(win, BLUE, (80, 100, 100, 100))
        next_text = MAIN_FONT.render("NEXT", 1, WHITE)
        win.blit(next_text, (80 + (100 - next_text.get_width())//2, 100 + (100 - next_text.get_height())//2))
    else :
        pygame.draw.rect(win, GREY2, (65, 85, 130, 130))
        pygame.draw.rect(win, GREY1, (80, 100, 100, 100))
        next_text = MAIN_FONT.render("NEXT", 1, WHITE)
        win.blit(next_text, (80 + (100 - next_text.get_width())//2, 100 + (100 - next_text.get_height())//2))
 

    if item == 1 :
        pygame.draw.rect(win, GREEN, (225, 85, 130, 130))
    else :
        pygame.draw.rect(win, DARK_BLUE, (225, 85, 130, 130))       
    pygame.draw.rect(win, BLUE, (240, 100, 100, 100))
    end_text = MAIN_FONT.render("END", 1, WHITE)
    win.blit(end_text, (240 + (100 - end_text.get_width())//2, 100 + (100 - end_text.get_height())//2))

    if item == 2 :
        pygame.draw.rect(win, GREEN, (385, 85, 130, 130))
    else :
              pygame.draw.rect(win, DARK_BLUE, (385, 85, 130, 130))  
    pygame.draw.rect(win, BLUE, (400, 100, 100, 100))
    quit_text = MAIN_FONT.render("QUIT", 1, WHITE)
    win.blit(quit_text, (400 + (100 - quit_text.get_width())//2, 100 + (100 - quit_text.get_height())//2))

def draw_menu(win, item) :
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

    titre = END_FONT.render("Puissance 4", 1, DARK_BLUE)
    win.blit(titre, ((WIDTH - titre.get_width())//2, 30))

    if item == 0 :
        pygame.draw.rect(win, GREEN, (300, 200, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 200, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 215, 370, 50))
    button0_text = MAIN_FONT.render("IA vs IA", 1, WHITE)
    win.blit(button0_text, (315 + (370 - button0_text.get_width())//2, 215 + (50 - button0_text.get_height())//2))

    if item == 1 :
        pygame.draw.rect(win, GREEN, (300, 300, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 300, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 315, 370, 50))
    button1_text = MAIN_FONT.render("Humain vs IA", 1, WHITE)
    win.blit(button1_text, (315 + (370 - button1_text.get_width())//2, 315 + (50 - button1_text.get_height())//2))

    if item == 2 :
        pygame.draw.rect(win, GREEN, (300, 400, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 400, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 415, 370, 50))
    button2_text = MAIN_FONT.render("Humain vs humain", 1, WHITE)
    win.blit(button2_text, (315 + (370 - button2_text.get_width())//2, 415 + (50 - button2_text.get_height())//2))

    if item == 3 :
        pygame.draw.rect(win, GREEN, (300, 500, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 500, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 515, 370, 50))
    button3_text = MAIN_FONT.render("Tournoi", 1, WHITE)
    win.blit(button3_text, (315 + (370 - button3_text.get_width())//2, 515 + (50 - button3_text.get_height())//2))

    if item == 4 :
        pygame.draw.rect(win, GREEN, (300, 600, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 600, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 615, 370, 50))
    button4_text = MAIN_FONT.render("Combat global", 1, WHITE)
    win.blit(button4_text, (315 + (370 - button4_text.get_width())//2, 615 + (50 - button4_text.get_height())//2))

    if item == 5 :
        pygame.draw.rect(win, GREEN, (300, 700, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 700, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 715, 370, 50))
    button5_text = MAIN_FONT.render("Verification", 1, WHITE)
    win.blit(button5_text, (315 + (370 - button5_text.get_width())//2, 715 + (50 - button5_text.get_height())//2))

    if item == 6 :
        pygame.draw.rect(win, GREEN, (300, 800, 400, 80))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 800, 400, 80))       
    pygame.draw.rect(win, BLUE, (315, 815, 370, 50))
    button5_text = MAIN_FONT.render("Quitter", 1, WHITE)
    win.blit(button5_text, (315 + (370 - button5_text.get_width())//2, 815 + (50 - button5_text.get_height())//2))

    if item == 7 :
        pygame.draw.rect(win, GREEN, (50, 850, 100, 100))
    else :
        pygame.draw.rect(win, DARK_VIOLET, (50, 850, 100, 100))       
    pygame.draw.rect(win, VIOLET, (65, 865, 70, 70))

def draw_choice(win, item, offset, heuristiques, playing_heuristiques) :
    heurlist = sorted(list(heuristiques.keys()))

    n = len(heuristiques.keys())

    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

    choice_text = MENU_FONT.render("Choix des heuristiques", 1, BLUE)
    win.blit(choice_text, ((WIDTH - choice_text.get_width())//2, 50))

    '''
    Taille des cases : 100 - nom ( 600 ) - cases a cocher (200) - 100
    '''

    for i in range(min(6, n)) :
        heur = heurlist[i+offset]

        pygame.draw.rect(win, DARK_BLUE, (100, 140 + i*120, 600, 100))
        pygame.draw.rect(win, BLUE, (115, 155 + i*120, 570, 70))

        h_text = MAIN_FONT.render(heur, 1, WHITE)
        win.blit(h_text, (100 + (600 - h_text.get_width())//2,140 + i*120 + (100 - h_text.get_height())//2))

        if playing_heuristiques[0] == heurlist[i+offset] :
            pygame.draw.rect(win, GREEN, (720, 140 + i*120, 100, 100))
            pygame.draw.rect(win, DARK_GREEN, (735, 155 + i*120, 70, 70))
        else :
            if item == i+1 :
                pygame.draw.rect(win, GREEN, (720, 140 + i*120, 100, 100))
            else :
                pygame.draw.rect(win, DARK_BLUE, (720, 140 + i*120, 100, 100))
            pygame.draw.rect(win, BLUE, (735, 155 + i*120, 70, 70))

        if playing_heuristiques[1] == heurlist[i+offset] :
            pygame.draw.rect(win, GREEN, (840, 140 + i*120, 100, 100))
            pygame.draw.rect(win, DARK_GREEN, (855, 155 + i*120, 70, 70))
        else :
            if item == -i-1 :
                pygame.draw.rect(win, GREEN, (840, 140 + i*120, 100, 100))
            else :
                pygame.draw.rect(win, DARK_BLUE, (840, 140 + i*120, 100, 100))
            pygame.draw.rect(win, BLUE, (855, 155 + i*120, 70, 70))

    if item == 7 :
        pygame.draw.rect(win, GREEN, (720, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (720, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (735, 875, 70, 70))
    
    up_text = MAIN_FONT.render("down", 1, WHITE)
    win.blit(up_text, (720 + (100 - up_text.get_width())//2, 860 + (100 - up_text.get_height())//2))

    if item == -7 :
        pygame.draw.rect(win, GREEN, (840, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (840, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (855, 875, 70, 70))

    down_text = MAIN_FONT.render("up", 1, WHITE)
    win.blit(down_text, (840 + (100 - down_text.get_width())//2, 860 + (100 - down_text.get_height())//2))

    if item == 8 :
        pygame.draw.rect(win, GREEN, (300, 860, 400, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 860, 400, 100))
    pygame.draw.rect(win, BLUE, (315, 875, 370, 70))

    play_text = MAIN_FONT.render("Play !", 1, WHITE)
    win.blit(play_text, (300 + (400 - play_text.get_width())//2, 860 + (100 - play_text.get_height())//2))

def draw_verif(win, item, offset, heuristiques, verif) :
    heurlist = sorted(list(heuristiques.keys()))

    n = len(heuristiques.keys())

    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

    choice_text = MENU_FONT.render("Verification des heuristiques", 1, BLUE)
    win.blit(choice_text, ((WIDTH - choice_text.get_width())//2, 50))

    '''
    Taille des cases : 100 - nom ( 600 ) - cases a cocher (200) - 100
    '''

    for i in range(min(6, n)) :
        heur = heurlist[i+offset]

        pygame.draw.rect(win, DARK_BLUE, (100, 140 + i*120, 600, 100))
        pygame.draw.rect(win, BLUE, (115, 155 + i*120, 570, 70))

        h_text = MAIN_FONT.render(heur, 1, WHITE)
        win.blit(h_text, (100 + (600 - h_text.get_width())//2,140 + i*120 + (100 - h_text.get_height())//2))
        
        if verif[heur][1] :
            pygame.draw.rect(win, GREEN, (840, 140 + i*120, 100, 100))
            pygame.draw.rect(win, DARK_GREEN, (855, 155 + i*120, 70, 70))
        else :
            pygame.draw.rect(win, RED, (840, 140 + i*120, 100, 100))
            pygame.draw.rect(win, DARK_RED, (855, 155 + i*120, 70, 70))

        pygame.draw.rect(win, DARK_BLUE, (720, 140 + i*120, 100, 100))
        pygame.draw.rect(win, BLUE, (735, 155 + i*120, 70, 70))
        time_text = LITTLE_FONT.render(str(verif[heur][0]), 1, BLACK, YELLOW)
        win.blit(time_text, (720 + (100 - time_text.get_width())//2, 140 + i*120 + (100 - time_text.get_height())//2))

    if item == 7 :
        pygame.draw.rect(win, GREEN, (720, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (720, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (735, 875, 70, 70))
    
    up_text = MAIN_FONT.render("down", 1, WHITE)
    win.blit(up_text, (720 + (100 - up_text.get_width())//2, 860 + (100 - up_text.get_height())//2))

    if item == -7 :
        pygame.draw.rect(win, GREEN, (840, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (840, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (855, 875, 70, 70))

    down_text = MAIN_FONT.render("up", 1, WHITE)
    win.blit(down_text, (840 + (100 - down_text.get_width())//2, 860 + (100 - down_text.get_height())//2))

    if item == 8 :
        pygame.draw.rect(win, GREEN, (300, 860, 400, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 860, 400, 100))
    pygame.draw.rect(win, BLUE, (315, 875, 370, 70))

    play_text = MAIN_FONT.render("Exit", 1, WHITE)
    win.blit(play_text, (300 + (400 - play_text.get_width())//2, 860 + (100 - play_text.get_height())//2))

def draw_tournoi(win) :
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

def draw_results(win, results, offset,item) :
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20))

    sresults = sorted(list(results.keys()))[::-1]

    to_display = []

    for e in sresults :
        for f in results[e] :
            to_display.append(f + " : " + str(e))

    n = len(to_display)

    choice_text = MENU_FONT.render("Resultats", 1, BLUE)
    win.blit(choice_text, ((WIDTH - choice_text.get_width())//2, 50))

    '''
    Taille des cases : 100 - nom ( 600 ) - cases a cocher (200) - 100
    '''

    for i in range(min(6, n)) :
        heur = to_display[i+offset]

        pygame.draw.rect(win, DARK_BLUE, (100, 140 + i*120, 600, 100))
        pygame.draw.rect(win, BLUE, (115, 155 + i*120, 570, 70))

        h_text = MAIN_FONT.render(heur, 1, WHITE)
        win.blit(h_text, (100 + (600 - h_text.get_width())//2,140 + i*120 + (100 - h_text.get_height())//2))

    if item == 7 :
        pygame.draw.rect(win, GREEN, (720, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (720, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (735, 875, 70, 70))
    
    up_text = MAIN_FONT.render("down", 1, WHITE)
    win.blit(up_text, (720 + (100 - up_text.get_width())//2, 860 + (100 - up_text.get_height())//2))

    if item == -7 :
        pygame.draw.rect(win, GREEN, (840, 860, 100, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (840, 860, 100, 100))
    pygame.draw.rect(win, BLUE, (855, 875, 70, 70))

    down_text = MAIN_FONT.render("up", 1, WHITE)
    win.blit(down_text, (840 + (100 - down_text.get_width())//2, 860 + (100 - down_text.get_height())//2))

    if item == 8 :
        pygame.draw.rect(win, GREEN, (300, 860, 400, 100))
    else :
        pygame.draw.rect(win, DARK_BLUE, (300, 860, 400, 100))
    pygame.draw.rect(win, BLUE, (315, 875, 370, 70))

    play_text = MAIN_FONT.render("Exit", 1, WHITE)
    win.blit(play_text, (300 + (400 - play_text.get_width())//2, 860 + (100 - play_text.get_height())//2))

    return n

def selected_item(mouse_pos, state) :

    '''
     Renvoie la cellule selectionnee
     
     Si state == 0 (menu principal) :
       0 : IA vs IA
       1 : humain vs IA
       2 : humain vs humain
       3 : tournoi
       4 : combats globaux
       5 : verification
       6 : quitter
    
     Si state == 1 (jeu IA vs IA) :
       0 :  NEXT
       1 :  END
       2 :  QUIT
    '''
    
    if state == 0 :
        if 300 <= mouse_pos[0] <= 700 :
            if 200 <= mouse_pos[1] <= 280 :
                return 0
            if 300 <= mouse_pos[1] <= 380 :
                return 1
            if 400 <= mouse_pos[1] <= 480 :
                return 2
            if 500 <= mouse_pos[1] <= 580 :
                return 3
            if 600 <= mouse_pos[1] <= 680 :
                return 4
            if 700 <= mouse_pos[1] <= 780 :
                return 5
            if 800 <= mouse_pos[1] <= 880 :
                return 6
        if 50 <= mouse_pos[0] <= 150 and 850 <= mouse_pos[1] <= 950 :
            return 7
        return -1

    if state == 1 :
        if 85 <= mouse_pos[1] <= 85 + 130 :
            if 65 <= mouse_pos[0] <= 65+130 :
                return 0
            elif 225 <= mouse_pos[0] <= 225+130 :
                return 1
            elif 385 <= mouse_pos[0] <= 385+130 :
                return 2
        return -1

    if state == 2 :
        if 85 <= mouse_pos[1] <= 85 + 130 :
            if 65 <= mouse_pos[0] <= 65+130 :
                return 0
            elif 225 <= mouse_pos[0] <= 225+130 :
                return 1
            elif 385 <= mouse_pos[0] <= 385+130 :
                return 2
        return -1
    
    if state == 3 :
        if 85 <= mouse_pos[1] <= 85 + 130 :
            if 65 <= mouse_pos[0] <= 65+130 :
                return 0
            elif 225 <= mouse_pos[0] <= 225+130 :
                return 1
            elif 385 <= mouse_pos[0] <= 385+130 :
                return 2
        return -1
    
    if state == 5 :
        if 720 <= mouse_pos[0] <= 720 + 100 :
            if 140 + 6*120 <= mouse_pos[1] <= 140 + 6*120 + 100 :
                return 7

        if 840 <= mouse_pos[0] <= 840 + 100 :
            if 140 + 6*120 <= mouse_pos[1] <= 140 + 6*120 + 100 :
                return -7

        if 300 <= mouse_pos[0] <= 700 and 860 <= mouse_pos[1] <= 960 :
            return 8
        
        return 0

    if state == 6 :
        if 720 <= mouse_pos[0] <= 720 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return i+1

        if 840 <= mouse_pos[0] <= 840 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return -i-1

        if 300 <= mouse_pos[0] <= 700 and 860 <= mouse_pos[1] <= 960 :
            return 8
        
        if 100 <= mouse_pos[0] <= 280 and 860 <= mouse_pos[1] <= 960 :
            return 9

        return 0

    if state == 7 :
        if 720 <= mouse_pos[0] <= 720 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return i+1

        if 840 <= mouse_pos[0] <= 840 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return -i-1

        if 300 <= mouse_pos[0] <= 700 and 860 <= mouse_pos[1] <= 960 :
            return 8
        
        if 100 <= mouse_pos[0] <= 280 and 860 <= mouse_pos[1] <= 960 :
            return 9

        return 0

    if state == 8 :
        if 720 <= mouse_pos[0] <= 720 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return i+1

        if 840 <= mouse_pos[0] <= 840 + 100 :
            for i in range(7) :
                if 140 + i*120 <= mouse_pos[1] <= 140 + i*120 + 100 :
                    return -i-1

        if 300 <= mouse_pos[0] <= 700 and 860 <= mouse_pos[1] <= 960 :
            return 8
        
        return 0

def selected_column(mouse_pos) :
    if 260 <= mouse_pos[1] <= 260 + 720 :
        for i in range(7) :
            if 80 + 120 * i <= mouse_pos[0] <= 80 + 120 * (i + 1) :
                return i
    return -1

def jouer_coup(board, coup, player) :
    row = game.trouver_ligne_libre(board, coup)

    board[row][coup] = player

def deep_copy(L) :
    new_L = []

    for e in L :
        new_L.append(e.copy())
    
    return new_L

def random_boards(n) :
    boards = []

    for _ in range(n) :
        board = []
        for _ in range(6) :
            ligne = []
            for _ in range(7) :
               ligne.append(rd.choice(["X", "O", " "]))
            board.append(ligne.copy())
        boards.append(deep_copy(board))
    
    return boards

def match(h1, h2, heuristiques) :

    q = mp.Queue()
    
    p1 = mp.Process(target=game.jouer_match, args = (heuristiques, h1, h2, q, False, ))
    p2 = mp.Process(target=game.jouer_match, args = (heuristiques, h2, h1, q, False, ))

    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

    res = []
    while q.qsize() > 0 :
        res.append(q.get())

    return res

def tournoi(heuristiques) :
    results = {}

    n = len(heuristiques.keys()) - 2
    p = n**2
    print("0.00%")

    k = 0

    for h1 in heuristiques :
        for h2 in heuristiques :
            if "Emma" not in h1 and "Emma" not in h2 :
                results[(h1, h2)] = match(h1, h2, heuristiques)
                k += 1
                print(str(k/p*100   )[:4]+"%")

    return results

def verifyone(f, boards) :
    result = [0, True]

    n = len(boards)

    for board in boards :
        t1 = time.time()
        score = f(board, "X")
        t2 = time.time()

        if type(score) not in [int, float] :
            result[1] = False
        else :
            result[0] += t2 - t1
    
    result[0] = result[0] / n
    return result

def clean_results(results, heuristiques) :
    semicleaned = {}

    for h in heuristiques :
        semicleaned[h] = 0

    for result in results :
        for e in results[result] :
            semicleaned[e] += 1

    cleaned = {}

    for e in semicleaned :
        if semicleaned[e] not in cleaned :
            cleaned[semicleaned[e]] = [e]
        else :
            cleaned[semicleaned[e]].append(e)

    cleaned[float("inf")] = ["Emma"]

    return cleaned

def verifyall(heuristiques, boards) :
    # Dictionnaire verification :
    #   heuristique : [temps moyen, True/False : renvoit bien un nombre]
    verif = {}

    for heuristique in heuristiques :
        verif[heuristique] = verifyone(heuristiques[heuristique], boards)
    print(verif)
    return verif

def main() :
    # Liste les noms des fichiers dans le dossier heuristique dans la liste files
    files = os.listdir("heuristiques")

    # La ou seront toutes les fonctions
    heuristiques = {}

    for file in files :
        if file != "__init__.py" and file != "__pycache__":
            # On importe la fonction heuristique du fichier en lui donnant le nom qu'avait le fichier et on l'ajoute au dictionnaire des heuristiques en l'associant a son nom
            exec("from heuristiques." + file[:-3] + " import heuristique as " + file[:-3])
            exec("heuristiques[\"" + file[:-3] + "\"] = " + file[:-3])

    running = True
    clock = pygame.time.Clock()

    # Etats du jeu :
    #   0 : menu principal
    #   1 : IA vs IA
    #   2 : humain vs IA
    #   3 : humain vs humain
    #   4 : tournoi
    #   5 : combat global heuristiques
    #   6 : verification
    #   7 : choix d'une heuristique
    #   8 : choix de deux heuristiques

    game_state = 0
    playing_heuristiques = [sorted(list(heuristiques.keys()))[0],sorted(list(heuristiques.keys()))[0]]
    display_heuristiques = playing_heuristiques.copy()
    players = ["X","O"]


    board = []
    for _ in range(6) : 
        board.append([" "] * 7)

    tick = 0

    while running :
        tick = (tick + 1) % 30
        clock.tick(FPS)
        click = False
        
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT :
                running = False
                break
            if event.type == pygame.MOUSEBUTTONUP :
                if mouse_state[0] :
                    click = True

        item = selected_item(mouse_pos, game_state)
        column = selected_column(mouse_pos)

        if game_state == 0 :
            draw_menu(WIN, item)
            if click :
                if item == 0 :
                    players = ["X","O"]
                    finished = False
                    winner = None
                    game_state = 8
                    offset = 0
                    board = []
                    for _ in range(6) : 
                        board.append([" "] * 7)
                    turn = 0
                if item == 1 :
                    players = ["X","O"]
                    finished = False
                    winner = None
                    offset = 0
                    game_state = 7
                    human_begins = True
                    board = []
                    for _ in range(6) : 
                        board.append([" "] * 7)
                    turn = 0
                if item == 2 :
                    players = ["X","O"]
                    game_state = 3
                    finished = False
                    winner = None
                    board = []
                    for _ in range(6) : 
                        board.append([" "] * 7)
                    turn = 0
                if item == 3 :
                    game_state = 4
                if item == 4 :
                    game_state = 5
                    results = clean_results(tournoi(heuristiques), heuristiques)
                    print(results)
                    offset = 0
                if item == 5 :
                    rboards = random_boards(20)
                    verif = verifyall(heuristiques, rboards)
                    game_state = 6
                    offset = 0
                if item == 6 :
                    running = False
                    break
                if item == 7 :
                    global DARK_VIOLET
                    global DARK_BLUE 
                    global DARK_GREEN
                    global DARK_RED
                    global DARK_YELLOW
                    DARK_BLUE, DARK_VIOLET, DARK_GREEN, DARK_RED, DARK_YELLOW = DARK_VIOLET, DARK_GREEN, DARK_RED, DARK_YELLOW, DARK_BLUE
                    global BLUE
                    global VIOLET
                    global GREEN
                    global RED
                    global YELLOW
                    BLUE, VIOLET, GREEN, RED, YELLOW = VIOLET, GREEN, RED, YELLOW, BLUE
        
        elif game_state == 1 :
            draw_game(WIN, board, display_heuristiques[0], display_heuristiques[1], item, -1)
            
            if turn == 42  :
                finished = True
                winner = "Tie"

            if finished :
                if winner == "Tie" :
                    end_text = MAIN_FONT.render("Egalite !", 1, BLACK)
                else :
                    end_text = MAIN_FONT.render(winner + " win !", 1, BLACK)
                WIN.blit(end_text, (545, 85))

            if click :
                if (item == 0 and not finished):
                    jouer_coup(board, game.meilleur_coup(board, players[0], heuristiques[playing_heuristiques[0]]), players[0])

                    if game.check_win(board, players[0]) :
                        winner = playing_heuristiques[0]
                        finished = True

                    playing_heuristiques.reverse()
                    players.reverse()
                    turn += 1

                if item == 1 and not finished :

                    while (not game.check_win(board, players[1])) and turn < 42:
                        jouer_coup(board, game.meilleur_coup(board, players[0], heuristiques[playing_heuristiques[0]]), players[0])
                        playing_heuristiques.reverse()
                        players.reverse()
                        turn += 1
                        print(turn)
                    
                    finished = True
                    if turn == 42 :
                        winner = "Tie"
                    else :
                        winner = playing_heuristiques[1]

                if item == 2 :
                    playing_heuristiques = [sorted(list(heuristiques.keys()))[0],sorted(list(heuristiques.keys()))[0]]
                    display_heuristiques = playing_heuristiques.copy()
                    game_state = 0
                    players = ["X","O"]
        
        elif game_state == 2 :
            draw_game(WIN, board, display_heuristiques[0], display_heuristiques[1], item, column if playing_heuristiques[0] == "Human" else -1, hidenext=playing_heuristiques[0] == "Human")
            pygame.draw.rect(WIN, WHITE, (225, 85, 130, 130))

            if turn == 42  :
                finished = True
                winner = "Tie"

            if finished :
                if winner == "Tie" :
                    end_text = MAIN_FONT.render("Egalite !", 1, BLACK)
                else :
                    end_text = MAIN_FONT.render(winner + " win !", 1, BLACK)
                WIN.blit(end_text, (545, 85))

            if click :
                if item == 0 and not finished and playing_heuristiques[0] != "Human":
                    jouer_coup(board, game.meilleur_coup(board, players[0], heuristiques[playing_heuristiques[0]]), players[0])

                    if game.check_win(board, players[0]) :
                        winner = playing_heuristiques[0]
                        finished = True

                    playing_heuristiques.reverse()
                    players.reverse()
                    turn += 1

                if item == 2 :
                    playing_heuristiques = [sorted(list(heuristiques.keys()))[0],sorted(list(heuristiques.keys()))[0]]
                    display_heuristiques = playing_heuristiques.copy()              
                    game_state = 0
                    players = ["X","O"]

                if not finished and column != -1 and playing_heuristiques[0] == "Human" and game.trouver_ligne_libre(board, column) != None :
                    board[game.trouver_ligne_libre(board, column)][column] = players[0]

                    if game.check_win(board, players[0]) :
                        winner = "You"
                        finished = True

                    playing_heuristiques.reverse()
                    players.reverse()

                    turn += 1

        elif game_state == 3 :
            display_heuristiques = ["Joueur1", "Joueur2"]

            draw_game(WIN, board, display_heuristiques[0], display_heuristiques[1], item, column, hidenext=True)
            pygame.draw.rect(WIN, WHITE, (225, 85, 130, 130))
            pygame.draw.rect(WIN, WHITE, (65, 85, 130, 130))


            if turn == 42  :
                finished = True
                winner = "Tie"

            if finished :
                if winner == "Tie" :
                    end_text = MAIN_FONT.render("Egalite !", 1, BLACK)
                else :
                    end_text = MAIN_FONT.render(winner + " win !", 1, BLACK)
                WIN.blit(end_text, (545, 85))

            if click :

                if item == 2 :
                    playing_heuristiques = [sorted(list(heuristiques.keys()))[0],sorted(list(heuristiques.keys()))[0]]
                    display_heuristiques = playing_heuristiques.copy()              
                    game_state = 0
                    players = ["X","O"]

                if not finished and column != -1 and game.trouver_ligne_libre(board, column) != None :
                    board[game.trouver_ligne_libre(board, column)][column] = players[0]

                    if game.check_win(board, players[0]) :
                        winner = display_heuristiques[players[0] == "O"]
                        finished = True

                    playing_heuristiques.reverse()
                    players.reverse()

                    turn += 1
            
        elif game_state == 4 :
            game_state = 0
            print("J'ai pas eu le temps... :,(")

        elif game_state == 5 :
            n = draw_results(WIN, results, offset, item)

            if click :
                if item == 7 :
                    if offset < n - 6 :
                        offset += 1
                elif item == -7 :
                    if offset > 0 :
                        offset -= 1
                elif item == 8 :
                    game_state = 0

        elif game_state == 6 :

            draw_verif(WIN, item, offset, heuristiques, verif)

            if click :
                if item == 7 :
                    if offset < len(heuristiques.keys()) - 6 :
                        offset += 1
                elif item == -7 :
                    if offset > 0 :
                        offset -= 1
                elif item == 8 :
                    game_state = 0
                elif 1 <= item <= 6 :
                    playing_heuristiques[0] = sorted(list(heuristiques.keys()))[item+offset-1]
                    display_heuristiques[0] = playing_heuristiques[0]
                elif -6 <= item <= -1 :
                    playing_heuristiques[1] = sorted(list(heuristiques.keys()))[-item+offset-1]
                    display_heuristiques[1] = playing_heuristiques[1]
        
        elif game_state == 7 :

            draw_choice(WIN, item, offset, heuristiques, playing_heuristiques)
            if human_begins :
                pygame.draw.rect(WIN, WHITE, (720, 140, 100, 720))
            else :
                pygame.draw.rect(WIN, WHITE, (840, 140, 100, 720))

            if click :
                if item == 7 :
                    if offset < len(heuristiques.keys()) - 6 :
                        offset += 1
                elif item == - 7 :
                    if offset > 0 :
                        offset -= 1
                elif item == 8 :
                    if human_begins :
                        display_heuristiques = ["Human", display_heuristiques[1]]
                    else :
                        display_heuristiques = [display_heuristiques[0], "Human"]
                    playing_heuristiques = display_heuristiques.copy()
                    game_state = 2
                elif item == 9 :
                    human_begins = not human_begins
                elif 1 <= item <= 6 and not human_begins:
                    playing_heuristiques[0] = sorted(list(heuristiques.keys()))[item+offset-1]
                    display_heuristiques[0] = playing_heuristiques[0]
                elif -6 <= item <= -1 and human_begins :
                    playing_heuristiques[1] = sorted(list(heuristiques.keys()))[-item+offset-1]
                    display_heuristiques[1] = playing_heuristiques[1]
            # Bouton d'echange de qui commence :
            
            if item == 9 :
                pygame.draw.rect(WIN, GREEN, (100, 860, 180, 100))
            else :
                pygame.draw.rect(WIN, DARK_BLUE, (100, 860, 180, 100))
            pygame.draw.rect(WIN, BLUE, (115, 875, 150, 70))
            switch_text = MAIN_FONT.render("Switch", 1, WHITE)
            WIN.blit(switch_text, (100 + (180 - switch_text.get_width())//2, 860 + (100 - switch_text.get_height())//2))

        elif game_state == 8 :
            draw_choice(WIN, item, offset, heuristiques, playing_heuristiques)

            if click :
                if item == 7 :
                    if offset < len(heuristiques.keys()) - 6 :
                        offset += 1
                elif item == -7 :
                    if offset > 0 :
                        offset -= 1
                elif item == 8 :
                    game_state = 1
                elif 1 <= item <= 6 :
                    playing_heuristiques[0] = sorted(list(heuristiques.keys()))[item+offset-1]
                    display_heuristiques[0] = playing_heuristiques[0]
                elif -6 <= item <= -1 :
                    playing_heuristiques[1] = sorted(list(heuristiques.keys()))[-item+offset-1]
                    display_heuristiques[1] = playing_heuristiques[1]

        pygame.display.update()
    
if __name__ == "__main__" :
    main()
    pygame.quit()
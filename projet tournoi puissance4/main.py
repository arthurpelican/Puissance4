import os
import codeprof as game
import multiprocessing as mp

HELP_TEXT = '''

Liste complete des commandes valables :

 - clear                                   : efface l'ecran.

 - help                                    : affiche ce texte.

 - list                                    : affiche le nom de toutes les heuristiques chargees.

 - match heuristique1 heuristique2 vrai    : match aller retour entre deux heuristiques. 
                                             argument supplementaire pour voir le deroule du match.

 - setdepth n                              : regle la profondeur d'exploration de minimax a n.

 - quit                                    : quitte le programme.


'''

def setdepth(n) :
    try :
        depth = int(n)
        print("Profondeur de recherche mise a " + n + ".")
    except :
        print("L'argument que vous avez precise n'est pas un entier valide.")

def clear() :
    print("\n" * 50)

def quit() :
    print("Au revoir.")
    exit()

def help() :
    print(HELP_TEXT)

def match(h1, h2, heuristiques, show = False) :

    q = mp.Queue()
    
    p1 = mp.Process(target=game.jouer_match, args = (heuristiques, h1, h2, q, show, ))
    p2 = mp.Process(target=game.jouer_match, args = (heuristiques, h2, h1, q, show, ))

    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

    res = []
    while q.qsize() > 0 :
        res.append(q.get())

    if len(res) == 0 :
        print("Egalite !")
        return 0
    elif len(res) == 1 or res[0] == res[1]:
        print(res[0] + " gagne !")
        return 1 if res[0] == h1 else 2
    else :
        print("Egalite !")
        return 0

def tournoi(heuristiques) :
    results = {}

    for h1 in heuristiques :
        for h2 in heuristiques :
            results[(h1, h2)] = match(h1, h2, heuristiques, False)

    print(results)

def main() :

    depth = 2

    # Liste les noms des fichiers dans le dossier heuristique dans la liste files
    files = os.listdir("heuristiques")

    # La ou seront toutes les fonctions
    heuristiques = {}

    for file in files :
        if file != "__init__.py" and file != "__pycache__":
            # On importe la fonction heuristique du fichier en lui donnant le nom qu'avait le fichier et on l'ajoute au dictionnaire des heuristiques en l'associant a son nom
            exec("from heuristiques." + file[:-3] + " import heuristique as " + file[:-3])
            exec("heuristiques[\"" + file[:-3] + "\"] = " + file[:-3])


    # Boucle pour afficher le menu console :

    running = True

    while running :
        print(">>", end = " ")
        cmd = input().split()

        if len(cmd) == 0 : 
            pass
        else :
            match cmd[0] :

                case "quit" :
                    quit()
                
                case "help" :
                    help()

                case "clear" :
                    clear()

                case "setdepth" :
                    if len(cmd) < 2 :
                        print("Vous devez preciser un argument entier n.")
                    elif len(cmd) > 3 :
                        print("Cette commande ne prend en entree qu'un unique argument.")
                    else :
                        setdepth(cmd[1])

                case "match" :
                    if len(cmd) < 3 :
                        print("ERREUR : Cette commande necessite au moins deux arguments.")
                    elif cmd[1] not in heuristiques or cmd[2] not in heuristiques :
                        print("Les heuristiques que vous avez renseignees ne sont pas valable. Tapez list pour la liste des heuristiques valables.")
                    elif len(cmd) == 3 :
                        match(cmd[1], cmd[2],heuristiques)
                    else :
                        match(cmd[1],cmd[2], heuristiques, show=True)

                case "tournoi" :
                    tournoi(heuristiques)

                case "list" :
                    print("\n\t" + "\n\t".join(list(heuristiques.keys())) + "\n")

                case _ :
                    print("Cette commande n'existe pas, tapez help pour une liste de toutes les commandes valides.")


if __name__ == "__main__" :
    main()
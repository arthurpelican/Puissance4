import os

# Liste les noms des fichiers dans le dossier heuristique dans la liste files
files = os.listdir("heuristiques")

# La ou seront toutes les fonctions
functions = {}

for file in files :
    if file != "__init__.py" and file != "__pycache__":
        # On importe la fonction heuristique du fichier en lui donnant le nom qu'avait le fichier et on l'ajoute a la liste fonctions
        exec("from heuristiques." + file[:-3] + " import heuristique as " + file[:-3])
        exec("functions[\"" + file[:-3] + "\"] = " + file[:-3])

print(functions)
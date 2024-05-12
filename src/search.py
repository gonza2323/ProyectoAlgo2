import pickle
import re
from . import trie


def search(texto):

    with open('database.pkl','br') as file:
        T = pickle.load(file)

    # Saca todos los signos de puntuación
    texto = re.sub(r'[^\w\s]', '', texto)

    # Filtra mayúsculas (lower) y se genera una lista de cada palabra (split)
    textoDePalabras = texto.lower().split()
    
    print(len(trie.getWords(T)))
    for palabra in textoDePalabras:
        print(trie.getWordCountPerDocument(T, palabra))
    
    # TODO Debe imprimir "document not found" si no hay resultados

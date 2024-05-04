import pickle
import re
from . import trie


def search(texto):
    print("Soy search")

    with open('Trie.pkl','br') as f:
        T=pickle.load(f)

    #Saca todos los signos de puntuacion
    texto=re.sub(r'[^\w\s]', '', texto)

    #Filtra mayusculas (lower) y se genera una lista de cada palabra (split)
    textoDePalabras=texto.lower().split()
    print(texto)
    print()
    print(textoDePalabras)

    print(len(trie.getWords(T)))
    for palabra in textoDePalabras:
        print(trie.search(T,palabra))

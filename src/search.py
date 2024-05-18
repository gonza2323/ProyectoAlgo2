import pickle
import re
from . import trie
from .database import *
from .filter_words import *


# Debe realizar la búsqueda del texto e imprimir los documentos relevantes en orden
def search(texto):

    # Esta función debería:

    # TODO Cargar una base de datos en lugar de un Trie y verificar que sea válida
    
    # TODO Filtar las palabras con filter_words(lista de las palabras)

    # TODO Calcular vector del texto de búsqueda
    # TODO función vectorize(texto) -> vector

    # TODO Estructura que guarde el vector de cada documento (diccionario?)
    # TODO para cada palabra recorrer el trie e ir actualizando los vectores de los documentos
    # TODO update_vectors(Trie, vectors, word)

    # TODO Comparar el vector de búsqueda con el vector de cada documento
    # TODO Imprimir los documentos en orden de relevancia

    # TODO Debe imprimir "document not found" si no hay resultados
    
    with open('trie.pkl','br') as file:
        trie = pickle.load(file)

    with open('documents.pkl','br') as file:
        documents = pickle.load(file)

    db=Database()
    db.trie = trie
    db.documents = documents

    textoFiltrado=filter_words(texto)
    
    print(len(trie.getWords(db.trie)))
    for palabra in textoFiltrado:
        print(trie.getWordCountPerDocument(db.trie, palabra))

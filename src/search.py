import pickle
import re
from . import trie
from filter_words import *


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


    with open('database.pkl','br') as file:
        T = pickle.load(file)


    texto_de_palabras = filter_words(file)
    diccionario = frecuencia_palabras(texto_de_palabras)
        
    print(len(trie.getWords(T)))
    for palabra in texto_de_palabras:
        print(trie.getWordCountPerDocument(T, palabra))

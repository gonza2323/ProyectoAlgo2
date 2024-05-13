import pickle
import re
from . import trie


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

    # Saca todos los signos de puntuación
    texto = re.sub(r'[^\w\s]', '', texto)

    # Filtra mayúsculas (lower) y se genera una lista de cada palabra (split)
    textoDePalabras = texto.lower().split()
    
    print(len(trie.getWords(T)))
    for palabra in textoDePalabras:
        print(trie.getWordCountPerDocument(T, palabra))

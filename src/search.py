import pickle
import re
from . import trie
from .database import *
from .filter_words import *
import math


# Debe realizar la búsqueda del texto e imprimir los documentos relevantes en orden
def search(texto_busqueda: str):
    
    # TODO Verificar que la base de datos se cargó correctamente
    # TODO Debe imprimir "document not found" si no hay resultados relevantes
    
    db : Database = Database.load()

    texto_filtrado = filter_words(texto_busqueda)

    vector_busqueda = vectorize(texto_filtrado)
    vectores : dict[str, list[float]] = {}
    
    # Para cada palabra de la búsqueda buscamos matcheos en el trie
    # utilizando el algoritmo del primer argumento. Si da match,
    # se ejecuta la función del segundo argumento
    for palabra in vector_busqueda:
        db.trie.find_matches(palabra, update_vectors, vectores)
    
    normalize_vectors(vectores, db.documents)
    
    
    # Para cada vector de un documento, calculamos su divergencia Jensen Shanon
    # con respecto al vector del texto de búsqueda y guardamos los resultados
    resultados : tuple[str, float] = []

    for document, vector in vectores.items():
        resultados.append((document, jensen_shannon_divergence(vector, vector_busqueda)))
    
    # Ordenamos de forma ascendente según la divergencia Jensen Shannon
    resultados.sort(key = lambda documento: documento[1])


    # Imprimimos los resultados
    for resultado in resultados:
        print(resultado)
    

# Crea un diccionario donde cada key (palabra) es una componente
# y su valor (número) es la cantidad de veces que aparece en el texto.
# Solo se usa para el texto de búsqueda. Para los documentos se utiliza
# update_vectors() que es más eficiente.
def vectorize(texto : str) -> dict[str, float]:
    vector : dict[str, float] = {}

    total_word_count = 0

    for word in texto:
        if word in vector:
            vector[word] += 1
        else:
            vector[word] = 1
        total_word_count += 1
    
    for word, count in vector.items():
        vector[word] = count / total_word_count

    return vector


# Es llamada cuando se detecta un match entre una de las palabras de búsqueda
# y una de las palabras del Trie. Por cada documento en el que aparece la palabra,
# cargará en su vector, en la componente correspondiente a tal palabra, la cantidad
# de veces que aparece en él.
def update_vectors(vectors, word_node: TrieNode, search_word : str):
    for document, count in word_node.documents.items():
        if document in vectors:
            vector = vectors[document]
            vector[search_word] = count
        else:
            vectors[document] = {search_word: count}


# "Normaliza" el vector de un documento dividiendo por la cantidad
# de palabras que contiene (no es que deja la norma en 1)
def normalize_vectors(vectors, documents):
    for document, vector in vectors.items():
        total_count = documents[document]
        for word, count in vector.items():
            vector[word] = count / total_count


# TODO Calcula la divergencia de Jensen Shannon para dos vectores
def jensen_shannon_divergence(p, q):
    M : dict[str, float] = {}
    for word in q:
        if p[word]:
            M[word]=(p[word]+q[word])/2 #verificar que pasa si la palabra no esta en p
        else:
             M[word]=(q[word])/2
    
    KL_P_M=0
    KL_Q_M=0

    for word in M:
        if p[word] and q[word]:
            KL_P_M += p[word] * math.log2(p[word]/M[word])  #hay que verificar si la palabra esta en p
            KL_Q_M += q[word] * math.log2(q[word]/M[word])  #hay que verificar si la palabra esta en q
        elif p[word]:
            KL_P_M += p[word] * math.log2(p[word]/M[word])  #hay que verificar si la palabra esta en p
            KL_Q_M += 0
        elif q[word]:
            KL_P_M += 0                                       #hay que verificar si la palabra esta en p
            KL_Q_M += q[word] * math.log2(q[word]/M[word])
        else:
            KL_P_M += 0
            KL_Q_M += 0

    
    divergence=(KL_P_M + KL_Q_M)/2

    return divergence
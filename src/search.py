import pickle
import re
from . import trie
from .database import *
from .filter_words import *
import math


# Debe realizar la búsqueda del texto e imprimir los documentos relevantes en orden
def search(texto_busqueda: str):
    
    # TODO Verificar que la base de datos se cargó correctamente

    
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
        resultados.append((document, jaccard_similarity(vector, vector_busqueda, db.documents[document])))
    
    # Ordenamos de forma ascendente según la divergencia Jensen Shannon
    resultados.sort(key = lambda documento: documento[1],reverse= True)

    #Debe imprimir "document not found" si no hay resultados relevantes
    if not resultados:
        print("Document not found")

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
def update_vectors(vectors, word_node: TrieNode, search_word : str, similarity):
    #Cant de documentos donde la aparece la palabra
    cant_docs_presente = len(word_node.documents)
    for document, count in word_node.documents.items(): #{document:veces_que_repite}
        if document in vectors:
            vector = vectors[document]
            vector[search_word] = (count * similarity,cant_docs_presente)
        else:
            vectors[document] = {search_word: (count * similarity,cant_docs_presente)}
    


# Deja la integral de las funciones de distribución de probabilidad en 1
#vectores = {documento,{palabra,cuenta}}
#db_documents = {docuemnt,total_palabras}
#len(db_documents) = numero de documentos
#TF = numero de veces que aparece/total_palabras lo obtengo despues de que normalizo
#IDF = numero total de documentos/ numero de documentos que contienen el termino
def normalize_vectors(vectors, documents):
    total_docs = len(documents)
    for document, vector in vectors.items():
        total_count = documents[document]
        for word, (count, cant_docs_presente) in vector.items():
            tf = count/total_count
            idf = math.log2(total_docs/cant_docs_presente)
            vector[word] = tf*idf

    


# TODO Calcula la divergencia de Jensen Shannon para dos vectores
def jensen_shannon_divergence(p, q):
    M : dict[str, float] = {}
    
    for word in q:
        if p.get(word):
            M[word]=(p[word]+q[word])/2 #verificar que pasa si la palabra no esta en p
        else:
             M[word]=(q[word])/2
    
    KL_P_M=0
    KL_Q_M=0

    for word in M:
        if p.get(word) and q.get(word):
            KL_P_M += p[word] * math.log2(p[word]/M[word])  #hay que verificar si la palabra esta en p
            KL_Q_M += q[word] * math.log2(q[word]/M[word])  
        elif q.get(word):
            KL_P_M += 0                                       #hay que verificar si la palabra esta en q
            KL_Q_M += q[word] * math.log2(q[word]/M[word])
        
    divergence=(KL_P_M + KL_Q_M)/2

    return divergence

#jaccard similarity, recibe dos vectores, p es el vector del documento, y q el vector busqueda
#lo que hace es trabajar con la interseccion y la union de dos conjuntos
#en la interseccion se ve las palabras que comparten ambos vectores
#y en la union es las palabras de ambos, pero si estan en los dos no las va a poner dos veces

def jaccard_similarity(p,q,len_pdf):
    #jaccard similarity con peso 
    #interseccion= pesomin(palabra_vector_p, palabra_vector_q)
    #union = pesomax(palabras_vetor_p, palabra_vector_q)
    interseccion = 0
    union = 0
    for word in q:
        if p.get(word):
            interseccion += min(p[word], q[word])
            union += max(p[word],q[word])
        else:
            union += q[word]
    return interseccion/union

    # set1 = set(p.keys())
    # set2 = set(q.keys())
    # intersection = len(set1.intersection(set2))
    # print(p)
    # print(q)
    # if len(p) < len(q):
    #     union = len_pdf + (len(q)-len(p))
    # else: 
    #     union = len_pdf - len(q)

    # if union != 0:
    #     #print("U/I",intersection/union)
    #     return intersection/union
    # else:
    #     return 0

    


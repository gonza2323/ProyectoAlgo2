import pickle
import re
from . import trie
from .database import *
from .filter_words import *
import math

"""
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
    
    # Ordenamos de forma ascendente según jaccard similarity
    resultados.sort(key = lambda documento: documento[1],reverse= True)

    #Debe imprimir "document not found" si no hay resultados relevantes
    if not resultados:
        print("Document not found")

    # Imprimimos los resultados
    for resultado in resultados:
        print(resultado)
    
"""
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
    factor_longitud = max(len_pdf,len(q))/min(len_pdf,len(q))
    return (interseccion/union) * factor_longitud

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





def search(texto_busqueda: str):
    
    # TODO Verificar que la base de datos se cargó correctamente

    min_palabras = 30
    db : Database = Database.load()

    texto_filtrado = filter_words(texto_busqueda)
    #si el texto filtrado queda vacio no lo busco
    if len(texto_filtrado) > 0:

        vector_busqueda = vectorize(texto_filtrado)

        tf : dict[str , dict[str , int]] = {}
        tf1 : dict[str , dict[str , int]] = {}

        idf : dict[str , float] = {}
        idf1 : dict[str , float] = {}

        D=len(db.documents)

        documentos=db.documents
        #si tiene pocas palabras calculo con jaccard similarity
        if len(vector_busqueda) < min_palabras:
            #Se carga todos los nombre de los documentos al diccionario
            for document in db.documents:
                tf[document]={}

            #Se buscan las palabras del texto dado(palabras textuales)
            for word in texto_filtrado:
                diccionario=db.trie.get_word_count_per_document(word)
                #Se cargan todas las apariciones de la pabra en el segundo diccionario
                #Se normaliza
                if diccionario is not None:
                    for document, count in diccionario.items():
                        if tf.get(document) is not None:
                            vector=tf[document]
                            vector[word]=count/documentos[document]
                        else:
                            vector=tf[document]
                            vector[word]=0

            for word in texto_filtrado:
                cant=len(db.trie.get_word_count_per_document(word)) if db.trie.get_word_count_per_document(word) is not None else 0
                idf[word] = math.log(D/(1+cant),10)


            tf_idf : dict[str , dict[str , int]] = tf

            for word in texto_filtrado:
                diccionario=db.trie.get_word_count_per_document(word)
                if diccionario is not None:
                    for document in diccionario:
                        if tf_idf.get(document) is not None:
                            vector=tf_idf[document]
                            vector[word] *= idf[word]

            for word in texto_filtrado:
                cantidiad = texto_filtrado.count(word)
                vector_busqueda[word] = cantidiad
                vector_busqueda[word] *= idf[word]
            
            diccionarioDeresultados : dict[str , int] = {}
            mod=modulo_vectorial(vector_busqueda)

            for document, diccionario in tf_idf.items():
                if (modulo_vectorial(diccionario) * mod) != 0 :
                    diccionarioDeresultados[document] = productoPunto(diccionario, vector_busqueda) / (modulo_vectorial(diccionario) * mod)
                else:
                    diccionarioDeresultados[document] = productoPunto(diccionario, vector_busqueda) 

        #si tiene muchas palabras calculamos con similitud coseno
        else:
            for word in texto_filtrado:
                db.trie.find_matches(word, update_vectors, tf1)


            for word in texto_filtrado:
                idf1[word] = math.log(D/(1+cantidad(word,tf1)),10)

            tf_idf1 : dict[str , dict[str , int]] = tf1
            for word in texto_filtrado:
                for document, diccionario in tf_idf1.items():
                    if word in diccionario:
                        vector=diccionario[word]
                        lista = list(vector)    #hay que realizar el cambio de tupla a lista porque 
                        lista[0] *= idf1[word]  #no se puede cambiar los valores de una tupla
                        vector = tuple(lista)
                        diccionario[word] = vector
            for word in texto_filtrado:
                cantidiad = texto_filtrado.count(word)
                vector_busqueda[word] = cantidiad
                vector_busqueda[word] *= idf1[word]

            diccionarioDeresultados : dict[str , int] = {}
            mod=modulo_vectorial(vector_busqueda)

            for document, diccionario in tf_idf1.items():
                if (modulo_vectorial1(diccionario) * mod) != 0 :
                    diccionarioDeresultados[document] = productoPunto1(diccionario, vector_busqueda) / (modulo_vectorial1(diccionario) * mod)
                else:
                    diccionarioDeresultados[document] = productoPunto1(diccionario, vector_busqueda) 

        resultados : tuple[str, float] = []

        for document, value in diccionarioDeresultados.items():
            resultados.append((document,value))
        
        # Ordenamos de forma ascendente según jaccard similarity
        resultados.sort(key = lambda documento: documento[1],reverse= True)

        #Debe imprimir "document not found" si no hay resultados relevantes
        if not resultados:
            print("Document not found")

        # Imprimimos los resultados
        for resultado in resultados:
            print(resultado[0]) #solo muestro los documentos, no muestro el campo value
    else:
        print("texto de ingreso queda vacio")



def productoPunto(p, q):
    resultado=0
    for word in q:
        if p.get(word) and q.get(word):
            resultado += p[word] * q[word]
        else:
            resultado += 0
    return resultado

def productoPunto1(diccionario, q):
    resultado=0
    for word in q:
        if diccionario.get(word) and q.get(word):
            
            resultado += diccionario[word] [0] * q[word]
        else:
            resultado += 0
    return resultado


def modulo_vectorial(vector):
    return math.sqrt(sum(x**2 for x in vector.values()))

def modulo_vectorial1(diccionario):
    x=0
    count=0
    for value, cant in diccionario.values():
        x=value
        count += x**2
    return math.sqrt(count)

def cantidad(word,tf1):
    count=0
    for document, diccionario in tf1.items():
        if word in diccionario:
            count += 1
        """
        for palabra in diccionario:
            if word == palabra:
                count += 1
                break #si la encuentra una ves es suficiente
        """
    return count
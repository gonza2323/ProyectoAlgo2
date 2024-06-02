from .database import *
from .filter_words import *
import math


# Debe realizar la búsqueda del texto e imprimir los documentos relevantes en orden
def search(texto_busqueda: str):
    
    db : Database = Database.load()

    texto_filtrado = filter_words(texto_busqueda)

    #si el texto filtrado queda vacio no lo busco
    if len(texto_filtrado) == 0:
        print("Texto de ingreso queda vacío")
        return

    vector_busqueda = vectorize_search(texto_filtrado)
    vectores : dict[str, list[float]] = {}
    
    # Para cada palabra de la búsqueda buscamos matcheos en el trie
    # utilizando el algoritmo del primer argumento. Si da match,
    # se ejecuta la función del segundo argumento
    for palabra in vector_busqueda:
        db.trie.find_matches(palabra, update_vectors, vectores, db.documents)
    
    
    # Para cada vector de un documento, calculamos su divergencia Jensen Shanon
    # con respecto al vector del texto de búsqueda y guardamos los resultados
    resultados : tuple[str, float] = []

    for document, vector in vectores.items():
        resultados.append((document, jaccard2(vector, vector_busqueda)))
    
    # Ordenamos de forma ascendente según jaccard similarity
    resultados.sort(key = lambda documento: documento[1], reverse= True)

    #Debe imprimir "document not found" si no hay resultados relevantes
    if not resultados:
        print("Document not found")
        return

    # Imprimimos los resultados
    for resultado in resultados:
        print(resultado)
    

# Crea un diccionario donde cada key (palabra) es una componente
# y su valor (número) es la cantidad de veces que aparece en el texto.
# Solo se usa para el texto de búsqueda. Para los documentos se utiliza
# update_vectors(), que es más eficiente.
def vectorize_search(texto : str) -> dict[str, float]:
    vector : dict[str, float] = {}
    total_word_count = len(texto)

    for word in texto:
        vector[word] = vector.get(word, 0) + 1
        
    for word in vector:
        vector[word] = vector[word]/total_word_count
    return vector 

#Calculamos el promedio de las longitudes de los documentos para usarlo en el tf_mejorado
def average(documents):
    avg = 0
    for document in documents:
        avg += documents[document]
    avg = avg/len(documents)
    return avg

#con esta funcion mejoramos el tf para que asigne pesos a las palabras dependiendo de la longitud del documento
def tf_con_parametros(tf, total_count, k, avg):
    return tf/(tf+(k*total_count/avg))

# Es llamada cuando se detecta un match entre una de las palabras de búsqueda
# y una de las palabras del Trie. Por cada documento en el que aparece la palabra,
# actualiza en su vector, la componente correspondiente a la palabra de búsqueda,
# haciendo el cálculo de peso con tf-idf y la similitud del match.
def update_vectors(vectors, word_node: TrieNode, search_word : str, similarity, documents):
    #documents = {document:cant_de_palabras}
    #Cant de documentos donde la aparece la palabra
    cant_docs_presente = len(word_node.documents)
    total_docs = len(documents)
    for document, count in word_node.documents.items(): #word_node.documents={document:veces_que_repite_la_palabra}
        total_count = documents[document]
        tf = count/total_count
        tf_mejorado = tf_con_parametros(tf, total_count, total_docs, average(documents))
        idf = math.log2(total_docs/cant_docs_presente)
        if document in vectors:
            vector = vectors[document]
            vector[search_word] = vector.get(search_word, 0) + tf * idf * similarity
        else:
            vectors[document] = {search_word: tf_mejorado * idf * similarity}

def productoPunto(p, q):
    resultado=0
    for word in q:
        if p.get(word) and q.get(word):
            resultado += p[word] * q[word]
        
    return resultado

def sumatoria(vector):
    sum = 0
    for word in vector:
        sum += (vector[word])**2
    return sum

def jaccard2(p,q):
    producto_pq = productoPunto(p,q)
    return producto_pq/((sumatoria(p)+sumatoria(q))-producto_pq)
    

# jaccard similarity, recibe dos vectores, p es el vector del documento, y q el vector busqueda
# lo que hace es trabajar con la intersección y la union de dos conjuntos
# en la intersección se ve las palabras que comparten ambos vectores
# y en la union es las palabras de ambos, pero si están en los dos no las va a poner dos veces
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
    #Queremos ajustar la similitud teniendo en cuenta la longitud del texto de busqueda
    #usamos la funcion logaritmica para que este ajuste se haga de forma gradual a medida que aumenta la longitud del texto de busqueda
    #antes para el factor longitud no usabamos el logaritmo y para los casos en los que el texto de busqueda era muy corto el resultado no era muy preciso
    #al implementar la funcion logaritmica se suaviza el efecto de la diferencia de longitud
    factor_longitud = max(len_pdf,len(q))/min(len_pdf,len(q)) 
    #va a ser un numero mayor a 1 por lo que nunca vamos a tener log(0)
    return (interseccion/union) * math.log(factor_longitud)


# TODO Queda probar esta similaridad
def search_cosine_similarity(texto_busqueda: str):
    
    db : Database = Database.load()

    texto_filtrado = filter_words(texto_busqueda)


    vector_busqueda = vectorize_search(texto_filtrado)

    tf : dict[str , dict[str , int]] = {}
    tf1 : dict[str , dict[str , int]] = {}

    idf : dict[str , float] = {}
    idf1 : dict[str , float] = {}

    D=len(db.documents)

    documentos=db.documents
    con_levenshtein = True
    # Sin Levenshtein
    if not con_levenshtein:
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

    # Con Levenshtein
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
        resultados.append((document, value))


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

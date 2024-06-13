from .database import *
from .filter_words import *
import math


# Debe realizar la búsqueda del texto e imprimir los documentos relevantes en orden
def search(texto_busqueda: str):
    
    try:
        db : Database = Database.load()
    except Exception:
        print("Falló la carga de la base de datos")
        return

    texto_filtrado = filter_words(texto_busqueda)

    #si el texto filtrado queda vacio no lo busco
    if len(texto_filtrado) == 0:
        print("Texto de ingreso queda vacío")
        return

    vector_busqueda = vectorize_search(texto_filtrado)
    vectores : dict[str, list[float]] = {}
    
    # Para cada palabra de la búsqueda buscamos matcheos en el trie
    # Si da match, se ejecuta la función del segundo argumento
    # que actualiza los vectores de los documentos que vaya encontrando
    for palabra in vector_busqueda:
        db.trie.find_matches(palabra, update_vectors, vectores, db.documents)
    
    
    # Para cada vector de un documento, calculamos su similaridad jaccard
    # con respecto al vector del texto de búsqueda y guardamos los resultados
    resultados : tuple[str, float] = []

    for document, vector in vectores.items():
        resultados.append((document, jaccard_similarity(vector, vector_busqueda, db.documents[document])))
    
    # Ordenamos de forma ascendente según similitud jaccard
    resultados.sort(key = lambda documento: documento[1], reverse= True)

    # Debe imprimir "document not found" si no hay resultados relevantes
    if not resultados:
        print("Document not found")
        return

    # Imprimimos los resultados
    for resultado in resultados:
        print(resultado[0])
    

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


# Es llamada cuando se detecta un match entre una de las palabras de búsqueda
# y una de las palabras del Trie. Por cada documento en el que aparece la palabra,
# actualiza en su vector, la componente correspondiente a la palabra de búsqueda,
# haciendo el cálculo de peso con tf-idf y la similitud del match.
def update_vectors(vectors, word_node: TrieNode, search_word : str, similarity, documents):
    #Cant de documentos donde la aparece la palabra
    cant_docs_presente = len(word_node.documents)
    total_docs = len(documents)
    for document, count in word_node.documents.items(): #{document:veces_que_repite}
        total_count = documents[document]
        tf = count/total_count
        idf = math.log2(total_docs/cant_docs_presente)
        if document in vectors:
            vector = vectors[document]
            vector[search_word] = vector.get(search_word, 0) + tf * idf * similarity
        else:
            vectors[document] = {search_word: tf * idf * similarity}


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

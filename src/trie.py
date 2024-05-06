
ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos


class Trie:
    root = None


class TrieNode:
    parent = None
    children = None
    key = None
    isEndOfWord = False
    documents = None


# Devuelve el índice de un caracter alfanúmerico
# en el array de hijos de un TrieNode
def getIndexOfChar(char):
    return ord(char) - ord('a') if ord(char) > 64 else ord(char) - ord('0')


# Inserta una palabra en el trie, manteniendo registro
# de cuántas veces aparece en cada documento
# Devuelve True si fue exitoso
def insert(t, word, document):
    if not word or not t or not document:
        return False
    
    # Si no tiene raíz, la creamos
    if not t.root:
        t.root = TrieNode()
        t.root.children = [None] * ALPHABET_SIZE

    # Recorremos el árbol siguiendo la palabra a insertar
    # Si ya no existen sus caracteres, los vamos creando
    node = t.root
    word = word.lower()
    for char in word:
        indexChild = getIndexOfChar(char)
        nextNode = node.children[indexChild]
        if not nextNode:
            node.children[indexChild] = TrieNode()
            nextNode = node.children[indexChild]
            
            nextNode.children = [None] * ALPHABET_SIZE
            nextNode.key = char
            nextNode.parent = node
        node = nextNode
    
    # Marcamos al último nodo como fin de palabra
    node.isEndOfWord = True

    # Revisamos si existen documentos con esa palabra
    # y actualizamos o creamos un contador según corresponda
    if node.documents:
        if document in node.documents:
            node.documents[document] += 1
        else:
            node.documents[document] = 1
    else:
        node.documents = {document : 1}

    return True


def getWordCountPerDocument(t, word):
    if not t or not t.root or not word:
        return None
    
    # Recorremos el trie siguiendo la palabra
    node = t.root
    word = word.lower()
    for i, char in enumerate(word):
        node = node.children[getIndexOfChar(char)]
        if (not node or
            node.key != char or
            (i == len(word) - 1 and not node.isEndOfWord)):
            return None # Si no está la palabra

    # Si está la palabra retornamos el diccionario
    # de documentos y cantidad de apariciones
    return node.documents


# Retorna una lista con las palabras
# presentes en el trie
def getWords(T):
    if not T:
        return None
    
    words = []

    def getWordsNode(word, node):
        if node.key:
            word = word + node.key
        
        if node.isEndOfWord:
            words.append(word)
        
        for child in node.children:
            if child:
                getWordsNode(word, child)
    
    if T.root:
        getWordsNode("", T.root)
    
    return words


ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos


class Trie:
    root = None


class TrieNode:
    parent = None
    children = None
    key = None
    is_end_of_word = False
    documents = None


# Devuelve el índice de un caracter alfanumérico
# en el array de hijos de un TrieNode
def get_index_of_char(char):
    if char == 'ñ':
        return 26
    elif ord(char) > 64:
        return ord(char) - ord('a')
    else:
        return ord(char) - ord('0') + 27


# Inserta una palabra en el trie, manteniendo registro
# de cuántas veces aparece en cada documento
# Devuelve True si fue exitoso
def insert_word(t, word, frequency, document):
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
        index_of_child = get_index_of_char(char)
        nextNode = node.children[index_of_child]
        if not nextNode:
            node.children[index_of_child] = TrieNode()
            nextNode = node.children[index_of_child]
            
            nextNode.children = [None] * ALPHABET_SIZE
            nextNode.key = char
            nextNode.parent = node
        node = nextNode
    
    # Marcamos al último nodo como fin de palabra
    node.is_end_of_word = True

    # Revisamos si existen documentos con esa palabra
    # y actualizamos o creamos un contador según corresponda
    if node.documents:
        if document not in node.documents:
            node.documents[document] = frequency
    else:
        node.documents = {document : frequency}

    return True


def get_word_count_per_document(t: Trie, word: str):
    if not t or not t.root or not word:
        return None
    
    # Recorremos el trie siguiendo la palabra
    node : TrieNode = t.root
    word = word.lower()

    for i, char in enumerate(word):
        node = node.children[get_index_of_char(char)]
        if (not node or
            node.key != char or
            (i == len(word) - 1 and not node.is_end_of_word)):
            return None # Si no está la palabra

    # Si está la palabra retornamos el diccionario
    # de documentos y cantidad de apariciones
    return node.documents


# Retorna una lista con las palabras
# presentes en el trie
def get_words(T : Trie):
    if not T:
        return None
    
    words : list[str] = []

    def get_words_node(word : str, node : TrieNode):
        if node.key:
            word = word + node.key
        
        if node.is_end_of_word:
            words.append(word)
        
        for child in node.children:
            if child:
                get_words_node(word, child)
    
    if T.root:
        get_words_node("", T.root)
    
    return words

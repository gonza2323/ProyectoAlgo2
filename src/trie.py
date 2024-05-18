
ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos


class Trie:
    def __init__(self):
        self.root = TrieNode()


class TrieNode:
    def __init__(self):
        self.parent : TrieNode = None
        self.children : list[TrieNode] = [None for i in range(ALPHABET_SIZE)]
        self.key = None
        self.is_end_of_word : bool = False
        self.documents : dict[str, int] = None


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

    # Recorremos el árbol siguiendo la palabra a insertar
    # Si ya no existen sus caracteres, los vamos creando
    node = t.root
    word = word.lower()
    for char in word:
        index_of_child = get_index_of_char(char)
        next_node = node.children[index_of_child]
        
        if not next_node:
            next_node = TrieNode()
            next_node.key = char
            next_node.parent = node

            node.children[index_of_child] = next_node
            
        node = next_node
    
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

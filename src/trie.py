
ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos


class TrieNode:
    def __init__(self):
        self.parent : TrieNode = None
        self.children : list[TrieNode] = [None for i in range(ALPHABET_SIZE)]
        self.key = None
        self.is_end_of_word : bool = False
        self.documents : dict[str, int] = None


class Trie:
    def __init__(self):
        self.root = TrieNode()


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
    def insert_word(self, word, document):
        if not word:
            return False

        # Recorremos el árbol siguiendo la palabra a insertar
        # Si ya no existen sus caracteres, los vamos creando
        node = self.root
        word = word.lower()
        for char in word:
            index_of_child = Trie.get_index_of_char(char)
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
            if document in node.documents:
                node.documents[document] += 1
            else:
                node.documents[document] = 1
        else:
            node.documents = {document : 1}

        return True


    def get_word_count_per_document(self, word: str):
        if not word:
            return None
        
        # Recorremos el trie siguiendo la palabra
        node : TrieNode = self.root
        word = word.lower()

        for i, char in enumerate(word):
            node = node.children[Trie.get_index_of_char(char)]
            if (not node or
                node.key != char or
                (i == len(word) - 1 and not node.is_end_of_word)):
                return None # Si no está la palabra

        # Si está la palabra retornamos el diccionario
        # de documentos y cantidad de apariciones
        return node.documents


    # Retorna una lista con las palabras
    # presentes en el trie
    def get_words(self):        
        words : list[str] = []

        def get_words_node(word : str, node : TrieNode):
            if node.key:
                word = word + node.key
            
            if node.is_end_of_word:
                words.append(word)
            
            for child in node.children:
                if child:
                    get_words_node(word, child)
        
        get_words_node("", self.root)
        
        return words


    # TODO Encontrar matches basados en la distancia Levenstein
    # Por solo realiza match exacto.
    def find_matches(self, search_word, on_match_function, vectors):
        
        def recursive(node: TrieNode, current_word = '', i = -1):
            if not node:
                return
            
            if i == len(search_word):
                return

            if node.key:
                if node.key != search_word[i]:
                    return
            
            if node.is_end_of_word and i == len(search_word) - 1:
                on_match_function(vectors, node, search_word)
            
            for child in node.children:
                recursive(child, i = i + 1)

        recursive(self.root)

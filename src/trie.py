from .wagner_fisher import similitud
from .filter_words import MAX_WORD_LENGTH

ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos

MIN_SIMILARITY = 0.8 # TODO Utilizarla para corta ramas del trie
MAX_SIMILARITY = 0.9 # TODO Utilizarla para agregar todas las palabras de esa rama del trie sin seguir calculando similitud


class TrieNode:
    def __init__(self):
        self.parent : TrieNode = None
        self.children : dict[str, TrieNode] = {}
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
            if char in node.children:            
                next_node = node.children[char]
            else:
                next_node = TrieNode()
                next_node.key = char
                next_node.parent = node
                node.children[char] = next_node
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
            node = node.children[char] if node.children.get(char) is not None else None # Para que en caso de no encontrar siguiente letra no se rompa.
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


    # Recorrer el trie buscando palabras que se encuentren dentro de un rango
    # aceptado de similitud, basado en la distancia Levenshtein. Si ocurre un
    # match, se llama a la función on_match_function y se le pasa la palabra
    def find_matches(self, search_word, on_match_function, vectors):
    
        matrix = [[i + j for j in range(len(search_word) + 1)] for i in range(MAX_WORD_LENGTH + 1)]
        
        def tolerancia(len_current_word, len_search_word):
            return (len_current_word / len_search_word)/2

        def find_matches_recursive(matrix, node, current_word='', i=0):
            if node is None:
                return
            
            if node.key:
                current_word += node.key
                for j in range(1, len(search_word) + 1):
                    insertions = matrix[i-1][j] + 1     # Celda de arriba
                    deletions = matrix[i][j-1] + 1      # Celda a la izquierda
                    substitutions = matrix[i-1][j-1]    # Celda en diagonal
                    if search_word[j-1] != node.key:
                        substitutions += 1
                    matrix[i][j] = min(insertions, deletions, substitutions)
                
                distance = matrix[i][len(search_word)]
                max_distance = max(i, len(search_word))
                similarity = 1 - distance/max_distance

                # print(f"current: {current_word}")
                # print(f"search: {search_word}")
                if similarity >= MIN_SIMILARITY:
                    if node.is_end_of_word:
                        #print(search_word, current_word, round(similarity, 3), distance, max_distance)
                        on_match_function(vectors, node, search_word, similarity)

                if similarity < MIN_SIMILARITY:
                    tol = tolerancia(len(current_word), len(search_word))
                    if similarity < tol: return

            for child in node.children.values():
                find_matches_recursive(matrix, child, current_word, i + 1)

        find_matches_recursive(matrix, self.root)
    
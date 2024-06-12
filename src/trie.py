from .filter_words import MAX_WORD_LENGTH


ALPHABET_SIZE = 27 + 10     # 27 letras, 10 dígitos
MIN_SIMILARITY = 0.8        # Mínima similitud utilizada en Levenshtein


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


    # Recorrer el trie buscando palabras que se encuentren dentro de un rango
    # aceptado de similitud, basado en la distancia Levenshtein. Si ocurre un
    # match, se llama a la función on_match_function y se le pasa la palabra
    def find_matches(self, search_word, on_match_function, vectors, documents):
    
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
                        on_match_function(vectors, node, search_word, similarity, documents)

                if similarity < MIN_SIMILARITY:
                    tol = tolerancia(len(current_word), len(search_word))
                    if similarity < tol: return

            for child in node.children.values():
                find_matches_recursive(matrix, child, current_word, i + 1)

        find_matches_recursive(matrix, self.root)
    
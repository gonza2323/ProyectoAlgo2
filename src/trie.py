from .filter_words import MAX_WORD_LENGTH


MIN_SIMILARITY = 0.8        # Mínima similitud Levenshtein para un match


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
    def insert_word(self, word, document):
        if not word:
            return False

        # Recorremos el árbol siguiendo la palabra a insertar
        # Si no existen sus caracteres, los vamos agregando al trie
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
        
        # Matriz para algoritmo Wagner-Fischer
        matrix = [[i + j for j in range(len(search_word) + 1)] for i in range(MAX_WORD_LENGTH + 1)]

        def find_matches_recursive(matrix, node, current_word='', i=0):
            if node is None:
                return
            
            if node.key:
                current_word += node.key

                # Calculamos la fila actual de la matriz
                for j in range(1, len(search_word) + 1):
                    insertions = matrix[i-1][j] + 1     # Celda de arriba
                    deletions = matrix[i][j-1] + 1      # Celda a la izquierda
                    substitutions = matrix[i-1][j-1]    # Celda en diagonal
                    if search_word[j-1] != node.key:
                        substitutions += 1
                    matrix[i][j] = min(insertions, deletions, substitutions)
                
                # Calculamos la similitud
                distance = matrix[i][len(search_word)]
                max_distance = max(i, len(search_word))
                similarity = 1 - distance/max_distance

                # Si es palabra y cumple el mínimo, añadimos a los vectores
                if similarity >= MIN_SIMILARITY and node.is_end_of_word:
                    on_match_function(vectors, node, search_word, similarity, documents)

                # Verificamos is podemos descartar lo que queda de esta parte del trie
                if similarity < MIN_SIMILARITY:
                    tolerancia = (len(current_word) / len(search_word)) / 2
                    if similarity < tolerancia: return

            # Seguimos recorriendo el trie
            for child in node.children.values():
                find_matches_recursive(matrix, child, current_word, i + 1)

        # Recorremos el trie desde la raíz
        find_matches_recursive(matrix, self.root)
    

class Trie:
    root = None


class TrieNode:
    parent = None
    children = None
    key = None
    isEndOfWord = False

ALPHABET_SIZE = 26

# --- Ejercicio 1a
def insert(T, element):
    if not element or not T:
        return None
    
    if not T.root:
        T.root = TrieNode()
        T.root.children = [None] * ALPHABET_SIZE

    node = T.root
    element = element.lower()
    for i, char in enumerate(element):
        indexChild = ord(char) - ord('a')
        nextNode = node.children[indexChild]
        if not nextNode:
            node.children[indexChild] = TrieNode()
            nextNode = node.children[indexChild]
            nextNode.children = [None] * ALPHABET_SIZE
            nextNode.key = char
            nextNode.parent = node
        if i == len(element) - 1:
            nextNode.isEndOfWord = True
        node = nextNode

    return None
# --- end


# --- Ejercicio 1b
def search(T, element):
    return bool(_findLastNodeOfWord(T, element))


def _findLastNodeOfWord(T, element):    
    if not T or not T.root or not element:
        return False
    
    node = T.root
    element = element.lower()
    for i, char in enumerate(element):
        node = node.children[ord(char) - ord('a')]
        if (not node or
            node.key != char or
            (i == len(element) - 1 and not node.isEndOfWord)):
            return False

    return node
# --- end


# --- Ejercicio 3
def delete(T, element):
    if not T or not T.root or not element:
        return False
    
    node = _findLastNodeOfWord(T, element) # final de palabra, si existe

    if not node:
        return False # Si no existe, no hacemos nada
    
    node.isEndOfWord = False

    # Mientras no tenga hijos ni sea fin de otra palabra, borramos nodo:
    while (not any(child for child in node.children) and not node.isEndOfWord):
        node.parent.children[ord(node.key)-ord('a')] = None # borramos el nodo
        node = node.parent # pasamos a su padre

    return True
# --- end


# --- Ejercicio 4
def printWordsWithPrefixAndLength(t, prefix, length):
    if not t or not t.root or not prefix or not length:
        return
    
    # Si el prefijo es mayor al largo de
    # palabra, retornamos
    if length < len(prefix):
        return
    
    # Encontrar node final del prefijo
    node = t.root
    prefix = prefix.lower()
    for c in prefix:
        node = node.children[ord(c) - ord('a')]
        if not node or node.key != c:
            return
    
    # Imprime palabras a partir de un nodo,
    # que tengan el largo indicado
    def printWordsFromNodeWithLength(node, word):
        if not node:
            return
        
        # Si llegamos al largo indicado,
        # imprimimos si es final de palabra
        # Si no, cortamos
        if len(word) == length:
            if node.isEndOfWord:
                print(word)
            return
        
        # Si todavía no llegamos al largo indicado
        # recorremos cada hijo del nodo
        for child in node.children:
            if child:
                printWordsFromNodeWithLength(child, word + child.key)

    # Imprimimos palabras del largo indicado
    # partiendo desde el final del prefijo
    printWordsFromNodeWithLength(node, prefix)
# --- end


# --- Ejercicio 5
def areEqual(t1, t2):
    if not t1 or not t2:
        return False
    
    # Caso trivial, referencias al mismo dato en memoria
    if t1 == t2:
        return True
    
    # Compara nodo a nodo, recursivamente
    def compareTrees(node1, node2):
        # Si ambos son None
        if not node1 and not node2:
            return True
        
        
        # Si uno es None y el otro no
        if not node1 or not node2:
            return False
        
        
        # Si difieren en alguna forma
        if (node1.key != node2.key
            or node1.isEndOfWord != node2.isEndOfWord
            or len(node1.children) != len(node2.children)):
            return False
        
        # Comparar hijos
        for i in range(len(node1.children)):
            # Si alguno difiere, ya podemos retornar falso
            if not compareTrees(node1.children[i], node2.children[i]):
                return False
        
        # Se cumplió todo, retornamos que son iguales
        return True
    
    # Comparamos ambos árboles a partir de la raíz
    return compareTrees(t1.root, t2.root)
# --- end


# --- Ejercicio 6
def hasInvertedWords(t):
    if not t or not t.root:
        return None
    
    # Recorremos el trie
    def traverseTrie(word, node):
        if not node:
            return False
        
        # Vamos calculando la palabra actual
        if node.key:
            word = word + node.key
        
        # Si es final de palabra, buscamos su inverso en el trie
        # Si está, retornamos verdadero, si no, revisamos los hijos
        if node.isEndOfWord and search(t, word[::-1]):
            return True

        # Retornamos si se cumple para alguno de sus hijos
        return any([traverseTrie(word, child) for child in node.children])

    return traverseTrie("", t.root)
# --- end


# --- Ejercicio 7
def autoCompletar(t, cadena):
    if not t or cadena is None:
        return None
    
    result = ""

    # Buscamos el último nodo de la cadena
    # Retornamos string vacío "" si no está
    node = t.root
    cadena = cadena.lower()
    for char in cadena:
        node = node.children[ord(char) - ord('a')]
        if (not node or node.key != char):
            return result

    while True:
        # Obtenemos los hijos que existen
        notNoneChildren = [child for child in node.children if child]
        
        # Si hay distinto de 1, o el nodo actual es final de palabra
        # retornamos el resultado actual
        if len(notNoneChildren) != 1 or node.isEndOfWord:
            break

        # Si no, sumamos la siguiente letra al resultado
        onlyChild = notNoneChildren[0]
        result += onlyChild.key
        node = onlyChild

    return result
# --- end


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

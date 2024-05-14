
from .trie import Trie

class Database:
    trie : Trie = None
    documents : dict[str, int] = None
    
    # Añade un documento a la base de datos
    # Debe actualizar tanto al Trie como al diccionario de documentos
    # Debería usar filter_words en algún momento
    # Retorna si fue exitoso o no
    def add_document(self, document_path : str) -> bool:
        pass

    # Guarda la base de datos en disco
    def save(self):
        pass

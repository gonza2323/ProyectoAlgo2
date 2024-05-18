
from .trie import *
from .filter_words import *
import os
import PyPDF2
from unidecode import unidecode
import pickle

class Database:
    trie : Trie = Trie()
    documents : dict[str, int] = {}
    
    # Añade los archivos pdf de la carpeta a la base de datos
    def add_documents(self, documentos):
        
        for archivo_pdf in documentos:
        # Obtener el nombre del archivo (sin la extensión) para usar como nombre de archivo de texto
            nombre_archivo = os.path.splitext(os.path.basename(archivo_pdf))[0]
        
            # Abre el archivo PDF en modo lectura binaria
            with open(archivo_pdf, 'rb') as pdf_file:
                # Crea un objeto PdfReader
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Inicializa una lista para almacenar el texto extraído de cada página
                texto_paginas = []

                # Itera sobre cada página del PDF
                for pagina_num in range(len(pdf_reader.pages)):
                    # Obtiene la página actual
                    pagina = pdf_reader.pages[pagina_num]

                    # Extrae el texto de la página y agrega cada línea a la lista texto_paginas
                    texto_paginas.extend(pagina.extract_text().splitlines())
                
            # Concatena todas las líneas de texto en una sola cadena sin saltos de línea
            texto_plano = ' '.join(texto_paginas)


            self.add_document(texto_plano,nombre_archivo)
            

    # Añade un documento a la base de datos
    def add_document(self, document_path : str, nombre_archivo) -> bool:

        print(f"Procesando archivo \"{nombre_archivo}\".")

        #Termina saca todas las palabras no deseadas
        palabras_procesadas = filter_words(document_path)


        # print(frecuencia_palabras(palabrasProcesadas))

        #Obtenemos la cantidad de palabra por texto
        total_palabras = len(palabras_procesadas)

        for palabra in palabras_procesadas:
        #    frecuenciaDePalabra=frecuencia_palabra(palabra,palabrasProcesadas)
           insert_word(self.trie, palabra, 1, nombre_archivo)

        self.documents[nombre_archivo] = total_palabras

        print(f"Archivo \"{nombre_archivo}\" guardado en la base de datos.")

        

    # Guarda la base de datos en disco
    def save(self):
        with open('trie.pkl','bw') as file:
            pickle.dump(self.trie, file)
        
        with open('documents.pkl','bw') as file:
            pickle.dump(self.documents, file)

        print("document data-base created successfully")
    

    # Carga la base de datos desde el disco
    def load():
        with open('trie.pkl','br') as file:
            trie = pickle.load(file)

        with open('documents.pkl','br') as file:
            documents = pickle.load(file)
        
        db = Database()
        db.trie = trie
        db.documents = documents
        
        return db


from .trie import *
from .filter_words import *
import os
import PyPDF2
from unidecode import unidecode
import pickle

class Database:
    trie : Trie = Trie()
    documents : dict[str, int] = {}
    
    # Añade un documento a la base de datos
    # Debe actualizar tanto al Trie como al diccionario de documentos
    # Debería usar filter_words en algún momento
    # Retorna si fue exitoso o no 

    def loop(self,directorios):
        
        for archivo_pdf in directorios:
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

            print(texto_plano)

            self.add_document(texto_plano,nombre_archivo)
            


    def add_document(self, document_path : str, nombre_archivo) -> bool:


        #Termina saca todas las palabras no deseadas
        palabrasProcesadas=filter_words(document_path)
        print(palabrasProcesadas)

        print(frecuencia_palabras(palabrasProcesadas))

        #Obtenemos la cantidad de palabra por texto
        totalPalabras=len(palabrasProcesadas)

        for palabra in palabrasProcesadas:
           frecuenciaDePalabra=frecuencia_palabra(palabra,palabrasProcesadas)
           insert(self.trie, palabra, frecuenciaDePalabra, nombre_archivo)

        self.documents[nombre_archivo]=totalPalabras

        print(f"Se guardo el {nombre_archivo} en la base de dato")

        

    # Guarda la base de datos en disco
    def save(self):

        T=self.trie
        document=self.documents
        
        with open('trie.pkl','bw') as f:
            pickle.dump(T,f)
        
        with open('document.pkl','bw') as f:
            pickle.dump(document,f)

        print("document data-base created successfully")


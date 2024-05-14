
from .trie import *
from .filter_words import *
import os
import PyPDF2
import re
from unidecode import unidecode
import pickle

class Database:
    trie : Trie = Trie()
    documents : dict[str, int] = {}
    
    # Añade un documento a la base de datos
    # Debe actualizar tanto al Trie como al diccionario de documentos
    # Debería usar filter_words en algún momento
    # Retorna si fue exitoso o no sdsds

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

            self.add_document(texto_plano,nombre_archivo)
            print("paso por aca")


    def add_document(self, document_path : str, nombre_archivo) -> bool:

        # Saca las tildes
        texto_sin_tilde=unidecode(document_path)

        # Saca todos los signos de puntuacion
        texto_sin_tilde=re.sub(r'[^\w\s]', '', texto_sin_tilde)

        # Filtra mayúsculas (lower) y se genera una lista de cada palabra (split)
        listaDePalabras=texto_sin_tilde.lower().split()

        #Termina saca todas las palabras no deseadas
        listaDePalabraProcesadas=filter_words(listaDePalabras)

        #Obtenemos la cantidad de palabra por texto
        totalPalabras=len(listaDePalabraProcesadas)

        for palabra in listaDePalabraProcesadas:
            if len(palabra)>5:
                insert(self.trie, palabra[0:4], nombre_archivo)
            else:
                insert(self.trie, palabra, nombre_archivo)

        self.documents[nombre_archivo]=totalPalabras

        with open('database.pkl','bw') as f:
            pickle.dump(self,f)

    # Guarda la base de datos en disco
    def save(self):
        
        with open('database.pkl','bw') as f:
            pickle.dump(self,f)
            

        print("Se guardo")

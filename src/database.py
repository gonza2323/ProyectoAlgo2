from .trie import *
from .filter_words import *
import os
import PyPDF2
import pickle


class Database:

    DATABASE_PATH = "./database.pkl"
    
    # Constructor
    def  __init__(self):
        self.trie : Trie = Trie()
        self.documents : dict[str, int] = {}

    
    # Añade los pdf encontrados en las direcciones contenidas en 'documentos'.
    def add_documents(self, documentos):
        
        for archivo_pdf in documentos:
            
            # Obtener el nombre del archivo (sin la extensión) para usar como nombre de archivo de texto
            nombre_archivo = os.path.splitext(os.path.basename(archivo_pdf))[0]
            print(f"Procesando archivo \"{nombre_archivo}\".")

            try:
                with open(archivo_pdf, 'rb') as pdf_file:
                    # Crea un objeto PdfReader
                    pdf_reader = PyPDF2.PdfReader(pdf_file)

                    for pagina in pdf_reader.pages:
                        texto_pagina = pagina.extract_text()
                        self.add_page(texto_pagina, nombre_archivo)
                    
                    print(f"Archivo \"{nombre_archivo}\" guardado en la base de datos.")

            except Exception as error:
                print(f"Ocurrió un error inesperado con el archivo {nombre_archivo}: {error}")
                

    # Añade un documento a la base de datos
    def add_page(self, document_path : str, nombre_archivo) -> bool:

        #Termina saca todas las palabras no deseadas
        palabras_procesadas = filter_words(document_path)

        #Obtenemos la cantidad de palabra en la página
        total_palabras = len(palabras_procesadas)

        for palabra in palabras_procesadas:
            self.trie.insert_word(palabra, nombre_archivo)
        
        if total_palabras > 0:
            self.documents[nombre_archivo] = self.documents.get(nombre_archivo, 0) + total_palabras
        

    # Guarda la base de datos en disco
    def save(self):
        with open(Database.DATABASE_PATH, "bw") as file:
            pickle.dump(self, file)

        print("document data-base created successfully")
    

    # Carga la base de datos desde el disco
    def load():
        try: 
            with open(Database.DATABASE_PATH, "br") as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f"No se encontró la base de datos en \"{Database.DATABASE_PATH}\"")
            raise
        except pickle.UnpicklingError:
            print(f"Error deserializando la base de datos \"{Database.DATABASE_PATH}\"")
            raise
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")
            raise

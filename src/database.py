
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

            try: #aca intenta abrir el archivo pdf

                # Abre el archivo PDF en modo lectura binaria
                with open(archivo_pdf, 'rb') as pdf_file:
                    # Crea un objeto PdfReader
                    pdf_reader = PyPDF2.PdfReader(pdf_file)

                    # Inicializa una lista para almacenar el texto extraído de cada página
                    texto_paginas = []

                    # Itera sobre cada página del PDF
                    for pagina in pdf_reader.pages:
                        #Extrae el texto de la pagina actual 
                        text_pagina = pagina.extract_text()
                        
                        if text_pagina:
                            #Dividir el texto en palabras y agrega las palabras a la lista
                            texto_paginas.extend(text_pagina.split())
                                        
                # Concatena todas las líneas de texto en una sola cadena sin saltos de línea
                texto_plano = ' '.join(texto_paginas)
                self.add_document(texto_plano, nombre_archivo)

            except Exception as error:
                print(f"Ocurrió un error inesperado con el archivo {nombre_archivo}: {error}")
                

    # Añade un documento a la base de datos
    def add_document(self, document_path : str, nombre_archivo) -> bool:

        #Termina saca todas las palabras no deseadas
        palabras_procesadas = filter_words(document_path)

        #Obtenemos la cantidad de palabra por texto
        total_palabras = len(palabras_procesadas)

        #verificar que si el documento quedo vacio, no lo añado a la base de datos
        if total_palabras > 0: #si es mayor a cero lo guarda en el trie, sino return
            for palabra in palabras_procesadas:
                self.trie.insert_word(palabra, nombre_archivo)

            self.documents[nombre_archivo] = total_palabras
            print(f"Archivo \"{nombre_archivo}\" guardado en la base de datos.")
        

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
        #caso en el que el archivo especificado no se encuentra en el directorio
        #no existe la base de datos 
            print("El archivo no fue encontrado")
        except pickle.UnpicklingError:
        #ocurrio un error durante el proceso de deserializacion del archivo .pkl
        #falla la carga de la base de datos 
            print("Error deserializando el archivo")
        except Exception as error:
        #ocurre cualquier otro error que no sea ninguno de los anteriores
        #por ejemplo: no se tienen permisos para leer el archivo, no hay suficiente memoria para cargar el archivo
        #muestra los detalles del error 
            print(f"Ha ocurrido un error inesperado: {error}")

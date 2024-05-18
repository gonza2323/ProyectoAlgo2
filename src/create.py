import os
import glob
import PyPDF2
from .trie import *
from unidecode import unidecode
import re
import pickle
from filter_words import *


def create(directorio_pdf: str):

    # Esta función debería:

    # TODO Crear base de datos
    
    # Cargar los documentos del directorio
    
    # TODO Para cada documento database.add_file(document).
    # document debería ser la dirección del archivo a cargar y que la clase
    # database se encargue de limpiarlo y añadirlo
    
    # TODO Si salió bien, guardar la base de datos al disco database.save()

    # TODO Imprimir si fue exitoso

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = glob.glob(os.path.join(directorio_pdf, '*.pdf'))
    
    T = Trie()

    # Recorrer cada archivo PDF
    for archivo_pdf in archivos_pdf:
        # Obtener el nombre del archivo (sin la extensión) para usar como nombre de archivo de texto
        nombre_archivo = os.path.splitext(os.path.basename(archivo_pdf))[0]
        
        # Ruta completa del archivo de texto a crear en el mismo directorio que el PDF
        ruta_txt = os.path.join(directorio_pdf, f'{nombre_archivo}.txt')

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
        
        #filtramos los pdf
        lista_de_palabras = filter_words(texto_plano)

        for palabra in lista_de_palabras:
            insert(T, palabra, nombre_archivo)
                    
        print(f'Texto extraído del archivo "{archivo_pdf}" y guardado en "{ruta_txt}"')

    with open('database.pkl','bw') as f:
        pickle.dump(T,f)

    print("document data-base created successfully")

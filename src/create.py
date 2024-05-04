import os
import glob
import PyPDF2
from . import trie
from unidecode import unidecode
import re
import pickle




def create(ruta):
    print("Soy un create")
    # Directorio donde se encuentran los archivos PDF
    directorio_pdf = ruta

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = glob.glob(os.path.join(directorio_pdf, '*.pdf'))
    
    T=trie.Trie()

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

        
        #Saca las tildes
        texto_sin_tilde=unidecode(texto_plano)

        #Saca todos los signos de puntuacion
        texto_sin_tilde=re.sub(r'[^\w\s]', '', texto_sin_tilde)

        #Filtra mayusculas (lower) y se genera una lista de cada palabra (split)
        listaDePalabras=texto_sin_tilde.lower().split()

        for palabra in listaDePalabras:
            trie.insert(T,palabra)
                    


        print(f'Texto extraído del archivo "{archivo_pdf}" y guardado en "{ruta_txt}"')

    with open('Trie.pkl','bw') as f:
        pickle.dump(T,f)

    print("document data-base created successfully")

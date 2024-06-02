import os
import glob
from .trie import *
from .database import *


def create(directorio_pdf: str):

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = glob.glob(os.path.join(directorio_pdf, '*.pdf'))

    #si la carpeta contiene archivos .pdf los agrega a la base de datos
    if archivos_pdf:
        db = Database()

        db.add_documents(archivos_pdf)

        db.save()
    else:
        print(f"la carpeta {directorio_pdf} no contiene archivos pdf")
    
    #si queremos dejar la base de datos vacia habria que sacar el if-else y cargar una carpeta vacia
    #ya que como esta la condicion no vuelve a editar el archivo a menos que la carpeta contenga un archivo .pdf

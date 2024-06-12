import os
import glob
from .trie import *
from .database import *


def create(directorio_pdfs: str):

    # Validación
    if not os.path.exists(directorio_pdfs):
        print(f"La ubicación {directorio_pdfs} no existe")
        return
    
    if not os.path.isdir(directorio_pdfs):
        print(f"{directorio_pdfs} no es una carpeta. Debe especificar una carpeta")
        return

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = glob.glob(os.path.join(directorio_pdfs, '*.pdf'))

    if not archivos_pdf:
        print(f"La carpeta {directorio_pdfs} no contiene archivos pdf")
        return

    db = Database()
    db.add_documents(archivos_pdf)
    db.save()

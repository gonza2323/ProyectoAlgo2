import os
import glob
from .trie import *
from .database import *


def create(directorio_pdf: str):

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = glob.glob(os.path.join(directorio_pdf, '*.pdf'))
    
    db = Database()

    db.loop(archivos_pdf)
    
    db.save()

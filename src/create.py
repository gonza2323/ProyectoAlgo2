import os
import glob
import PyPDF2
from .trie import *
from unidecode import unidecode
import re
import pickle
from .database import *


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
    
    db=Database()

    db.loop(archivos_pdf)
    
    db.save()


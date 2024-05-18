from unidecode import unidecode
import re

MAX_WORD_LENGTH = 20

# Filtra un texto según el criterio que decidamos
# Debe retornar una lista de palabras
def filter_words(texto_plano) -> list[str]:
    # Saca las tildes
    texto_sin_tilde = unidecode(texto_plano)
    # Saca todos los signos de puntuación
    texto_sin_tilde = re.sub(r'[^\w\s]', '', texto_sin_tilde)
    # Filtra mayúsculas (lower) y se genera una lista de cada palabra (split)
    lista_de_palabras = texto_sin_tilde.lower().split()

    #L: lista de palabras vacías
    stop_words = ['el', 'la', 'lo', 'los', 'las', 'un', "una", "unos", "uno", "unas", "a", "ante", "cabe", "con", 
            "contra", "de", "desde", "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", 
            "segun", "sin", "si", "ni", "so", "sobre", "tras", "al", "del", "y", "o", "que", "esto", "esta", 
            "este", "eso", "ese", "esa", "aquello", "aquel", "aquella", "estos", "estas", "alli", "esos", "esas", 
            "alla", "aquellos", "aquellas",'yo', 'tu', 'el', 'ella', 'usted', 'nosotros', 'nosotras', 'vosotros', 
            'vosotras', 'ellos', 'ellas', 'ustedes','me', 'te', 'nos', 'os', 'alguno', 'alguna', 'algo', 'ninguno', 'ninguna',
            'nadie', 'otro', 'otra', 'cualquier', 'quienquiera','algunos', 'algunas', 'nada', 'ningunos', 'ningunas', 'nadie', 
            'otros', 'otras', 'cualesquiera']

    lista_de_palabras = [palabra for palabra in lista_de_palabras if palabra not in stop_words]
    lista_de_palabras = [palabra[0:MAX_WORD_LENGTH] if len(palabra) > MAX_WORD_LENGTH else palabra for palabra in lista_de_palabras]
    
    return lista_de_palabras


def frecuencia_palabras(lista_de_palabras) -> dict:
    diccionario = {}
    for palabra in lista_de_palabras:
        diccionario[palabra] = round(lista_de_palabras.count(palabra)/len(lista_de_palabras), 4)
    return diccionario


def frecuencia_palabra(palabra, lista_de_palabras) -> dict:
    frecuencia = round(lista_de_palabras.count(palabra)/len(lista_de_palabras), 4)
    return frecuencia

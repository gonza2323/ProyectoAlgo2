from unidecode import unidecode
import re

# Filtra una lista de palabras según el criterio que decidamos
# Debe retornar también una lista de palabras, con raices
def filter_words(texto_plano) -> list[str]:
    # Saca las tildes
    texto_sin_tilde=unidecode(texto_plano)
    # Saca todos los signos de puntuacion
    texto_sin_tilde=re.sub(r'[^\w\s]', '', texto_sin_tilde)
    # Filtra mayúsculas (lower) y se genera una lista de cada palabra (split)
    listaDePalabras=texto_sin_tilde.lower().split()
    print(listaDePalabras)

    #L: lista de palabras vacias
    stop_words = ['el', 'la', 'lo', 'los', 'las', 'un', "una", "unos", "uno", "unas", "a", "ante", "cabe", "con", 
            "contra", "de", "desde", "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", 
            "segun", "sin", "si", "ni", "so", "sobre", "tras", "al", "del", "y", "o", "que", "esto", "esta", 
            "este", "eso", "ese", "esa", "aquello", "aquel", "aquella", "estos", "estas", "alli", "esos", "esas", 
            "alla", "aquellos", "aquellas",'yo', 'tu', 'el', 'ella', 'usted', 'nosotros', 'nosotras', 'vosotros', 
            'vosotras', 'ellos', 'ellas', 'ustedes','me', 'te', 'nos', 'os', 'alguno', 'alguna', 'algo', 'ninguno', 'ninguna',
            'nadie', 'otro', 'otra', 'cualquier', 'quienquiera','algunos', 'algunas', 'nada', 'ningunos', 'ningunas', 'nadie', 
            'otros', 'otras', 'cualesquiera']

    listaDePalabras = [palabra for palabra in listaDePalabras if palabra not in stop_words]
    listaDePalabras = [palabra[0:5] if len(palabra) > 5 else palabra for palabra in listaDePalabras]
    print(listaDePalabras)
    return listaDePalabras

def frecuencia_palabras(listaDePalabras) -> dict:
    
    diccionario = {}
    for palabra in listaDePalabras:
        diccionario[palabra] = round(listaDePalabras.count(palabra)/len(listaDePalabras), 4)
    print(f"diccionario: {diccionario}")
    return diccionario

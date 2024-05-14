
# Filtra una lista de palabras según el criterio que decidamos
# Debe retornar también una lista de palabras
NoWords=['yo', 'tu', 'el', 'ella', 'usted', 'nosotros', 'nosotras', 'vosotros', 'vosotras', 'ellos', 'ellas', 'ustedes','me', 'te', 'lo', 'la', 'nos', 'os', 'los', 'las',
         'este', 'esta', 'esto', 'estos', 'estas','ese', 'esa', 'eso', 'esos', 'esas','aquel', 'aquella', 'aquello', 'aquellos', 'aquellas',
         'alguno', 'alguna', 'algo', 'ninguno', 'ninguna', 'nadie', 'otro', 'otra', 'cualquier', 'quienquiera','algunos', 'algunas', 'nada', 'ningunos', 'ningunas', 'nadie',
         'otros', 'otras', 'cualesquiera', 'quienesquiera','que', 'quien', 'cual','quienes', 'cuales','mi', 'tu', 'su', 'nuestro', 'vuestro', 'mis', 'tus', 'sus', 'nuestros', 'vuestros'
         'cuanto', 'cuanta','cuales', 'cuantos', 'cuantas'
         ]

def filter_words(lista_de_palabras : list[str]) -> list[str]:
    
    filtrado=[]

    for palabras in lista_de_palabras:
        if palabras not in NoWords:
            filtrado.append(palabras)

    return filtrado

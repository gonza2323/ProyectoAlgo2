def distancia_wagner_fisher(str_corta,str_larga) -> int:
#implementamos el algoritmo de wagner fisher optimizado (reduce el espacio de almacenamiento de O(m*n) a O(min(m,n))
#usamos solo dos vetores fila en lugar de una matriz
#se coloca la palabra mas corta de forma horizontal y la mas larga en vertical 

    #ns aseguramos que las palabras se encuentren en sus respectivas variables de acuerdo a la longitud
    if len(str_corta) > len(str_larga):
        str_corta, str_larga = str_larga, str_corta
    
    len_str_corta = len(str_corta)
    len_str_larga = len(str_larga)
            
    #definimos dos vectores fila: prev y current, que seran de tamaño len_str_corta
    current = [i for i in range(len_str_corta+1)]

    for i in range(1,len_str_larga+1):
        prev = current
        current = [i] + ([0] * (len_str_corta))
        
        for j in range(1,len_str_corta+1):
            add = prev[j] +1 #justo arriba
            delete = current[j-1] + 1 #a la izquierda
            change = prev[j-1] #diagonal hacia arriba
            if str_corta[j-1] != str_larga[i-1]: #si los caracteres son iguales no se requiere hacer ninguna operacion (add, delete, change)
                change += 1 
            current[j] = min(add,delete,change)
        #print(f"current: {current}")

    distance = current[len_str_corta]
    return distance
    

def similitud(str1,str2) -> float:
    distancia = distancia_wagner_fisher(str1,str2)
    indice_similitud = 1 - (distancia/max(len(str1),len(str2)))
    indice_similitud  = round(indice_similitud,3)
    return indice_similitud

#Una forma común de normalizar la distancia de Levenshtein es convertirla en una similitud en el rango de 0 a 1,
#donde 1 significa que las palabras son idénticas y 0 significa que no tienen ninguna similitud.
    # similitud = 1 - (distancia W-F / max(len_str1, len_str2))

print(similitud("campa","campamento")) #si (0.5)
print(similitud("mercado","mercaderia")) #si (0.6)
print(similitud("cartera","carro")) #no (0.5)
print(similitud("camino","cama")) #no (0.5)
print(similitud("camila","camisa")) #no (0.83)
print(similitud("bueno","buen"))


#!/usr/bin/env python3
from src import main
from sys import exit

# El archivo con el que se ejecuta el programa es solo un wrapper que
# llama al código que se encuentra en 'main', dentro del paquete 'src'
# El código principal tiene que estar en un paquete de Python (una carpeta)
# para poder importarlo en los tests. De otra forma, no se puede testear.
main.main()

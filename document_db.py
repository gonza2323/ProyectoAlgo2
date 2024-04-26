import sys
from src import create, search

if len(sys.argv) < 3:
    print("Faltan argumentos")
    exit()

if sys.argv[1] == "-create":
    create.create()
elif sys.argv[1] == "-search":
    search.search()
else:
    print("No es un comando")
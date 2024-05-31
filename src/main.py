from sys import argv
from .create import create
from .search import search

def main(arguments = argv[1:]):
    
    # Verificar que se haya especificado un comando
    if len(arguments) < 1:
        print("Error. Debe especificar un comando. Use '-create' o '-search'.")
        return 1
    
    comando = arguments[0]

    if comando == "-create":
        if len(arguments) == 2:
            create(arguments[1])
        else:
            print("Error. Número incorrecto de argumentos. Use '-create <local_path>'")
            return 1

    elif comando == "-search":
        # Verificar que haya un solo argumento para '-search'
        #--------------------------------------------------------esta modificado el len
    
        if len(arguments) == 2:
            search(arguments[1])
        else:
            print("Error. Número incorrecto de argumentos. Use '-search <text>'")
            return 1
    else:
        print(f"Error. '{comando}' no es un comando válido. Use '-create' o '-search'")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())


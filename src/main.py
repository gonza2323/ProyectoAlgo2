from sys import argv
from .create import create
from .search import search


def main(arguments = argv[1:]):
    
    # Verificar que se haya especificado un comando
    if len(arguments) < 1:
        print("Error. Debe especificar un comando. Use '-create' o '-search'.")
        return
    
    comando = arguments[0]

    if comando == "-create":
        if len(arguments) == 2:
            create(arguments[1])
        else:
            print("Error. Número incorrecto de argumentos. Use '-create <local_path>'")
            return

    elif comando == "-search":
        # Verificar que haya un solo argumento para '-search'
        if len(arguments) == 2:
            search(arguments[1])
        else:
            print("Error. Número incorrecto de argumentos. Use '-search <text>'")
            return
    else:
        print(f"Error. '{comando}' no es un comando válido. Use '-create' o '-search'")
        return


if __name__ == "__main__":
    main()

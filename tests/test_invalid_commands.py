from src import main


def test_main_no_command(capsys):
    assert main.main([])

    out, _ = capsys.readouterr()
    assert out == "Error. Debe especificar un comando. Use '-create' o '-search'.\n"


def test_main_invalid_command(capsys):
    comando = '-asdf'
    assert main.main([comando])

    out, _ = capsys.readouterr()
    assert out == f"Error. '{comando}' no es un comando válido. Use '-create' o '-search'\n"


def test_main_create_wrong_no_of_arguments(capsys):
    assert main.main(["-create"])

    out, _ = capsys.readouterr()
    assert out == "Error. Número incorrecto de argumentos. Use '-create <local_path>'\n"

    assert main.main(["-create", "arg1", "arg2"])

    out, _ = capsys.readouterr()
    assert out == "Error. Número incorrecto de argumentos. Use '-create <local_path>'\n"


def test_main_search_wrong_no_of_arguments(capsys):
    assert main.main(["-search"])

    out, _ = capsys.readouterr()
    assert out == "Error. Número incorrecto de argumentos. Use '-search <text>'\n"

    assert main.main(["-search", "arg1", "arg2"])

    out, _ = capsys.readouterr()
    assert out == "Error. Número incorrecto de argumentos. Use '-search <text>'\n"

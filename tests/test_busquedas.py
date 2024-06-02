from src import main


def test_busquedas(capsys):
    query = """Uno de los viejos amigos de Belladona es un mago que se hace llamar Gandalf y que, aunque no tiene nada que hacer en
Hobbiton, un día aparece en la casa de Bilbo. Al principio, no parecen llevarse bien, ya que Gandalf es un extranjero y los
extranjeros no son respetados, puesto que pueden empujar a la gente respetable a cometer locuras. Cuando Gandalf revela su
identidad, Bilbo se muestra más educado y lo invita a tomar el té: recuerda a Gandalf haciendo fuegos artificiales durante las fiestas
y esto le genera cierta simpatía."""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "El Hobbit" in first_line, "Buscar un párrafo de 'El Hobbit' no devuelve 'El Hobbit' como primer resultado"


    query = """A lo lejos, un autogiro pasaba entre los tejados, se quedaba un instante colgadoen el aire y luego se lanzaba otra vez en un vuelo
curvo. Era de la patrulla de policía encargada devigilar a la gente a través de los balcones y ventanas. Sin embargo, las patrullas
eran lo de menos.Lo que importaba verdaderamente era la Policía del Pensamiento"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar un párrafo de '1984'-Español no devuelve '1984'-Español como primer resultado"


    query = """Cuando era un niño quería ser dibujante, pero los adultos lo disuadieron de su propósito. Encuentra en el principito a un amigo,
que entiende sus dibujos y le enseña, con sus historias y sus actos, el verdadero valor de las cosas. En el piloto se retrata la
importancia de seguir nuestros sueños."""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Principito" in first_line, "Buscar un párrafo de 'El Principito' no devuelve 'Principito' como primer resultado"


    query = """En la Tierra, entrará en contacto con animales, flores y personas. Será allí donde, antes de encontrar al piloto, conocerá al zorro,
quien le revelará la importancia de la amistad y el valor del amor que siente hacia su flor. Será la nostalgia por ella y la decepción
que le causa el mundo de los adultos lo que lo motivará a regresar a su planeta."""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Principito" in first_line, "Buscar un párrafo de un resumen de 'El Principito' no devuelve 'Principito' como primer resultado"


    query = "alan turing"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Alan Turing" in first_line, "Buscar 'alan turing' no devuelve el paper de Alan Turing"


    query = "Antoine De Saint Exupéry Antoine de Saint-Exupéry"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Principito" in first_line, "Buscar 'Antoine De Saint Exupéry' no devuelve 'Principito'"


    query = """Al momento, se le volvió roja la cara y los ojos empezaron a llorarle. Este líquido era comoácido nítrico; además, al tragarlo, se tenía la
misma sensación que si le dieran a uno un golpe en lanuca con una porra
de goma. Sin embargo, unos segundos después, desaparecía la incandescenciadel vientre y el mundo empezaba a resultar más alegre.
Winston sacó un cigarrillo de una cajetillasobre la cual se leía: Cigarrillos de la Victoria, y como lo tenía cogido verticalmente pordistracción,
se le vació en el suelo. Con el próximo pitillo tuvo ya cuidado y el tabaco no se salió.Volvió al cuarto de estar y se sentó ante una mesita
situada a la izquierda de la telepantalla. Delcajón sacó un portaplumas, un tintero y un grueso libro en blanco de tamaño in-quarto, con
ellomo rojo y cuyas tapas de cartón imitaban el mármol."""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar un párrafo de '1984'-Español no devuelve '1984'-Español como primer resultado"


    query = """El juego se ha convertido en espect·culo, con pocosprotagonistas y muchos
espectadores, f?tbol para mirar, y el espect·culo se ha convertido en uno de los negocios m·s lucrativos del mundo"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "El futbol a sol y sombra" in first_line, "Buscar un párrafo de 'El futbol a sol y sombra' no devuelve 'El futbol a sol y sombra' como primer resultado"


    query = "la guerra es la paz, la libertad es la esclavitud, la ignorancia es la fuerza"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar una frase de '1984'-Español no devuelve '1984'-Español como primer resultado"


    query = "deporte"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert ("futbol a sol y sombra" in first_line) or ("Ética y deporte" in first_line) or ("Fisiologia y Metodologia del Entrenamiento" in first_line), "Buscar 'deporte' no devuelve un artículo relacionado"


    query = "turing"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Alan Turing" in first_line, "Buscar 'turing' no devuelve el paper de Alan Turing"


    query = """Las personas mayores me aconsejaron abandonar el dibujo de serpientes boas, ya fueran abiertas o cerradas, yponer más interés en la
geografía, la historia, el cálculo y la gramática. De esta manera a la edad de seis añosabandoné una magnífica carrera de pintor. Había
quedado desilusionado por el fracaso de mis dibujos número 1y número 2. Las personas mayores nunca pueden comprender algo por sí solas
y es muy aburrido para los niñostener que darles una y otra vez explicaciones"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Principito" in first_line, "Buscar un párrafo de 'El Principito' no devuelve 'Principito' como primer resultado"


    query = """Es la primera obra que explora el universo mitológico creado por Tolkien y que más tarde se encargarían de definir El Señor de los
Anillos y El Silmarillion. Dentro de dicha ficción, el argumento de El hobbit se
sitúa en el año 2941 de la Tercera Edad del Sol,2? y narra la historia del hobbit Bilbo Bolsón, que junto con el mago Gandalf y un
grupo de enanos, vive una aventura en busca del tesoro custodiado por el dragón Smaug en la Montaña Solitaria."""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "El Hobbit" in first_line, "Buscar un párrafo de un resumen de 'El Hobbit' no devuelve 'El Hobbit' como primer resultado"


    query = """El mundo futurista de 1984 está dividido en tres superpotencias que viven
en permanente estado de guerra: Oceanía, Eurasia y Asia Oriental.La historia se desarrolla en Oceanía, que está conformada por
las regiones angloparlantes y regida por un Partido único. Este se divide en el Partido Interior que gobierna y constituye el 2% de la
población, y el Partido Exterior, que contiene al 13% y está encargado de ejecutar las órdenes. El resto de los habitantes
corresponde al proletariado,
quienes son ignorados porque el Partido considera que no tienen la capacidad intelectual necesaria para organizar una rebelión"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar un párrafo de un resumen de '1984'-Español no devuelve '1984'-Español como primer resultado"


    query = """Un elemento más viene a sumarse a las incógnitas. El concepto de «amorsocrático», de que algunos autores franceses han
abusado dándole unsignificado perverso, se ha identificado con las palabras textuales de laacusación, en el misterioso proceso del
filósofo, y ha surgido una nueva yfalsa interrogante: la de la homosexualidad. En los diálogos de Platón es muyfrecuente el tema de
las relaciones unisexuales; pero esto no prueba nadacontra el maestro"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "Enigmas de la historia" in first_line, "Buscar un párrafo de 'Enigmas de la historia' no devuelve 'Enigmas de la historia' como primer resultado"


    query = """A la espalda de Winston, la voz de la telepantalla seguía murmurando datos sobre el hierro yel cumplimiento del noveno Plan Trienal. La
telepantalla recibía y transmitía simultáneamente.Cualquier sonido que hiciera Winston superior a un susurro, era captado por el aparato.
Además,mientras permaneciera dentro del radio de visión de la placa de metal, podía ser visto a la vez queoído"""
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar un párrafo de '1984'-Español no devuelve '1984'-Español como primer resultado"
    
    
    query = "ministerio, verdad, paz, libertad, guerra"
    assert not main.main(["-search", query])
    out, _ = capsys.readouterr()
    first_line = out.strip().splitlines()[0]
    assert "1984 - Español" in first_line, "Buscar palabras clave de '1984'-Español no devuelve '1984'-Español como primer resultado"

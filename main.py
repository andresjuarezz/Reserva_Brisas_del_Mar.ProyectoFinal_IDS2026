from clases import Reserva

tipos = {
    "Individual": {"capacidad": 1, "precio": 50},
    "Pareja": {"capacidad": 2, "precio": 80},
    "Familiar": {"capacidad": 5, "precio": 130},
}

habitaciones = {
    "Individual": [101, 102],
    "Pareja": [201, 202],
    "Familiar": [301, 302],
}


def pedir_entero(mensaje, minimo, maximo):
    """Solicita un numero entero dentro del rango permitido."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: ingrese un numero entre {minimo} y {maximo}.")
        except ValueError:
            print("Error: debe ingresar un numero entero valido.")


def cargar():
    """Carga las reservas desde datos.py y devuelve una lista de Reserva."""
    reservas = []
    try:
        import datos

        for item in datos.reservas_guardadas:
            reserva = Reserva(
                item["numero"],
                item["nombre"],
                item["habitacion"],
                item["tipo"],
                item["personas"],
                item["plan"],
                item["llegada"],
                item["noches"],
            )
            reservas.append(reserva)
    except (ImportError, AttributeError, SyntaxError):
        print("No hay reservas guardadas. Se empieza vacío.")
    return reservas


def guardar(reservas):
    """Guarda la lista de objetos Reserva en datos.py."""
    with open("datos.py", "w", encoding="utf-8") as archivo:
        archivo.write("reservas_guardadas = [\n")
        for reserva in reservas:
            linea = repr(reserva.a_diccionario())
            archivo.write(f"    {linea},\n")
        archivo.write("]\n")
    print("Reservas guardadas correctamente en datos.py.")

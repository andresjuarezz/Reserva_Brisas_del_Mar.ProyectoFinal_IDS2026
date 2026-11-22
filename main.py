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


def habitaciones_libres(reservas, tipo, llegada, salida):
    """Retorna la lista de habitaciones disponibles para el tipo y rango de fechas."""
    libres = []
    for hab in habitaciones[tipo]:
        ocupada = False
        for r in reservas:
            if r.choca_con(hab, llegada, salida):
                ocupada = True
                break
        if not ocupada:
            libres.append(hab)
    return libres


def registrar(reservas):
    """Registra una nueva reserva validando las reglas R1 a R6."""
    print("\n--- Registrar Reserva ---")
    nombre = input("Nombre del huesped: ").strip()
    if nombre == "":
        print("Error (R1): el nombre del huesped no puede estar vacio.")
        return

    tipo = input("Tipo de habitacion (Individual, Pareja, Familiar): ").strip().title()
    if tipo not in tipos:
        print("Error (R2): tipo de habitacion invalido. Use Individual, Pareja o Familiar.")
        return

    capacidad = tipos[tipo]["capacidad"]
    personas = pedir_entero(f"Cantidad de personas (1-{capacidad}): ", 1, capacidad)

    print("Planes disponibles:")
    print("1. Solo habitacion")
    print("2. Todo incluido")
    plan_texto = input("Plan (1=Solo habitacion, 2=Todo incluido): ").strip().lower()
    if plan_texto == "1" or plan_texto == "solo habitacion" or plan_texto == "solo habitación":
        plan = "Solo habitacion"
    elif plan_texto == "2" or plan_texto == "todo incluido":
        plan = "Todo incluido"
    else:
        print("Error (R6): plan invalido. Elija Solo habitacion o Todo incluido.")
        return

    llegada = pedir_entero("Dia de llegada en diciembre (1-30): ", 1, 30)
    noches = pedir_entero("Cantidad de noches (1-7): ", 1, 7)
    salida = llegada + noches
    if salida > 31:
        print("Error (R3): la fecha de salida no puede pasar del 31 de diciembre.")
        return

    libres = habitaciones_libres(reservas, tipo, llegada, salida)
    if len(libres) == 0:
        print("Error (R4): no hay habitaciones disponibles de ese tipo para esas fechas.")
        return

    habitacion_asignada = libres[0]
    mayor = 0
    for r in reservas:
        if r.numero > mayor:
            mayor = r.numero
    nuevo_numero = mayor + 1

    nueva = Reserva(
        nuevo_numero,
        nombre,
        habitacion_asignada,
        tipo,
        personas,
        plan,
        llegada,
        noches,
    )
    reservas.append(nueva)

    precio_noche = tipos[tipo]["precio"]
    total = nueva.calcular_total(precio_noche)
    print("\nReserva confirmada:")
    print(f"Numero: {nuevo_numero}")
    print(f"Huesped: {nombre}")
    print(f"Habitacion asignada: {habitacion_asignada} ({tipo})")
    print(f"Personas: {personas} | Plan: {plan}")
    print(f"Estancia: del {llegada} al {salida} de diciembre ({noches} noches)")
    print(f"Total a pagar: ${total}")
    print("Horario informativo: Check-in desde las 15:00, Check-out hasta las 12:00.")

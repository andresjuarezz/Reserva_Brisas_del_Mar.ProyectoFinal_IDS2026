class Reserva:
    """Representa una reserva del Hotel Brisas del Mar para diciembre."""

    def __init__(self, numero, nombre, habitacion, tipo, personas, plan, llegada, noches):
        """Inicializa los datos de la reserva."""
        self.numero = numero
        self.nombre = nombre
        self.habitacion = habitacion
        self.tipo = tipo
        self.personas = personas
        self.plan = plan
        self.llegada = llegada
        self.noches = noches

    def salida(self):
        """Retorna el dia de salida calculado como llegada mas noches."""
        return self.llegada + self.noches

    def choca_con(self, habitacion, llegada, salida):
        """Verifica si esta reserva choca en habitacion y rango de fechas."""
        if self.habitacion != habitacion:
            return False
        return llegada < self.salida() and self.llegada < salida

    def calcular_total(self, precio_noche):
        """Calcula el costo total segun el plan de la reserva."""
        base = precio_noche * self.noches
        if self.plan == "Todo incluido":
            return base + 40 * self.personas * self.noches
        return base

    def a_diccionario(self):
        """Convierte la reserva en un diccionario."""
        return {
            "numero": self.numero,
            "nombre": self.nombre,
            "habitacion": self.habitacion,
            "tipo": self.tipo,
            "personas": self.personas,
            "plan": self.plan,
            "llegada": self.llegada,
            "noches": self.noches,
        }

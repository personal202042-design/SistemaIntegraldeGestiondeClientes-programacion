# Excepciones personalizadas para el sistema
class ClienteInvalidoError(Exception):
    """Excepción para datos de cliente inválidos."""
    pass

class ServicioNoDisponibleError(Exception):
    """Excepción cuando un servicio no está disponible."""
    pass

class ReservaInvalidaError(Exception):
    """Excepción para reservas con datos incorrectos."""
    pass

class DuracionInvalidaError(Exception):
    """Excepción para duración negativa o cero."""
    pass

class CapacidadExcedidaError(Exception):
    """Excepción cuando la capacidad de una sala es excedida."""
    pass
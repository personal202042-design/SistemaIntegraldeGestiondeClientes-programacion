from datetime import datetime
from excepciones import ReservaInvalidaError, ServicioNoDisponibleError, DuracionInvalidaError

class Reserva:
    _contador_id = 1
    
    def __init__(self, cliente, servicio, duracion, fecha=None, parametros_extra=None):
        self._id = Reserva._contador_id
        Reserva._contador_id += 1
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._fecha = fecha if fecha else datetime.now()
        self._estado = "PENDIENTE"
        self._parametros_extra = parametros_extra if parametros_extra else {}
        self._costo = None
        self._validar_reserva()
    
    def _validar_reserva(self):
        if not self._cliente:
            raise ReservaInvalidaError("La reserva debe tener un cliente valido.")
        if not self._servicio:
            raise ReservaInvalidaError("La reserva debe tener un servicio valido.")
        try:
            self._servicio.validar_disponibilidad()
        except ServicioNoDisponibleError as e:
            raise ReservaInvalidaError(f"Servicio no disponible: {e}") from e
        if self._duracion <= 0:
            raise DuracionInvalidaError(f"Duracion invalida: {self._duracion}")
    
    def confirmar(self):
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")
        self._estado = "CONFIRMADA"
        self._costo = self._servicio.calcular_costo(self._duracion, **self._parametros_extra)
    
    def cancelar(self):
        if self._estado == "CONFIRMADA":
            self._estado = "CANCELADA"
        elif self._estado == "CANCELADA":
            raise ReservaInvalidaError("La reserva ya está cancelada.")
        else:
            self._estado = "CANCELADA"
    
    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise ReservaInvalidaError("Solo se pueden procesar reservas confirmadas.")
        self._estado = "COMPLETADA"
    
    def get_costo(self):
        if self._costo is None and self._estado == "CONFIRMADA":
            self._costo = self._servicio.calcular_costo(self._duracion, **self._parametros_extra)
        return self._costo
    
    def get_id(self):
        return self._id
    
    def get_estado(self):
        return self._estado
    
    def __str__(self):
        return f"Reserva #{self._id}: {self._cliente.get_nombre()} - {self._servicio.get_nombre()} ({self._duracion} unidades) - {self._estado} - ${self.get_costo() if self._costo else 'N/A'}"
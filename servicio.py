from abc import ABC, abstractmethod
from excepciones import ServicioNoDisponibleError, DuracionInvalidaError, CapacidadExcedidaError

class Servicio(ABC):
    def __init__(self, codigo, nombre, disponible=True):
        self._codigo = codigo
        self._nombre = nombre
        self._disponible = disponible
    
    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo del servicio segun duracion y parametros adicionales."""
        pass
    
    @abstractmethod
    def describir(self):
        """Retorna descripcion del servicio."""
        pass
    
    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self._nombre} no esta disponible actualmente.")
    
    def get_codigo(self):
        return self._codigo
    
    def get_nombre(self):
        return self._nombre
    
    def is_disponible(self):
        return self._disponible
    
    def set_disponible(self, disponible):
        self._disponible = disponible

# Servicio especializado: Reserva de Salas
class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, capacidad_maxima, costo_por_hora, disponible=True):
        super().__init__(codigo, nombre, disponible)
        self._capacidad_maxima = capacidad_maxima
        self._costo_por_hora = costo_por_hora
    
    def calcular_costo(self, duracion, **kwargs):
        if duracion <= 0:
            raise DuracionInvalidaError(f"Duracion invalida: {duracion}. Debe ser positiva.")
        cantidad_personas = kwargs.get('cantidad_personas', 1)
        if cantidad_personas > self._capacidad_maxima:
            raise CapacidadExcedidaError(f"Capacidad excedida: {cantidad_personas} > {self._capacidad_maxima}")
        costo_base = duracion * self._costo_por_hora
        # Descuento por grupo grande (más de 10 personas)
        if cantidad_personas > 10:
            costo_base *= 0.9
        return round(costo_base, 2)
    
    def describir(self):
        return f"Sala '{self._nombre}', capacidad {self._capacidad_maxima} pers., ${self._costo_por_hora}/hora"

# Servicio especializado: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, costo_por_dia, requiere_deposito=True, disponible=True):
        super().__init__(codigo, nombre, disponible)
        self._costo_por_dia = costo_por_dia
        self._requiere_deposito = requiere_deposito
    
    def calcular_costo(self, duracion, **kwargs):
        if duracion <= 0:
            raise DuracionInvalidaError(f"Duracion invalida: {duracion} días.")
        costo = duracion * self._costo_por_dia
        if self._requiere_deposito:
            deposito = kwargs.get('deposito', 50)
            costo += deposito
        if kwargs.get('seguro', False):
            costo += 15
        return round(costo, 2)
    
    def describir(self):
        return f"Equipo '{self._nombre}', ${self._costo_por_dia}/día, Deposito: {self._requiere_deposito}"

# Servicio especializado: Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, costo_por_hora, nivel_experto="Junior", disponible=True):
        super().__init__(codigo, nombre, disponible)
        self._costo_por_hora = costo_por_hora
        self._nivel_experto = nivel_experto
    
    def calcular_costo(self, duracion, **kwargs):
        if duracion <= 0:
            raise DuracionInvalidaError(f"Duración invalida: {duracion} horas.")
        multiplicador = 1.0
        if self._nivel_experto == "Senior":
            multiplicador = 1.5
        elif self._nivel_experto == "Master":
            multiplicador = 2.0
        costo = duracion * self._costo_por_hora * multiplicador
        # Descuento por paquete de horas (>=5 horas)
        if duracion >= 5:
            costo *= 0.95
        return round(costo, 2)
    
    def describir(self):
        return f"Asesoria '{self._nombre}', nivel {self._nivel_experto}, ${self._costo_por_hora}/hora base"
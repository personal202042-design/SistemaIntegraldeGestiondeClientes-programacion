from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from excepciones import *
from logger_util import logger
import traceback

class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
    
    def registrar_cliente(self, nombre, email, telefono):
        try:
            cliente = Cliente(nombre, email, telefono)
            self.clientes.append(cliente)
            logger.info(f"Cliente registrado: {cliente.get_nombre()}")
            return cliente
        except ClienteInvalidoError as e:
            logger.error(f"Error registro cliente: {e}")
            raise ClienteInvalidoError(f"No se pudo registrar: {e}") from e
    
    def agregar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise TypeError("No es un servicio valido")
            self.servicios.append(servicio)
            logger.info(f"Servicio agregado: {servicio.get_nombre()}")
        except Exception as e:
            logger.error(f"Error agregar servicio: {e}")
            raise
    
    def buscar_servicio_por_codigo(self, codigo):
        for s in self.servicios:
            if s.get_codigo() == codigo:
                return s
        return None
    
    def buscar_cliente_por_nombre(self, nombre):
        for c in self.clientes:
            if c.get_nombre().lower() == nombre.lower():
                return c
        return None
    
    def crear_reserva(self, nombre_cliente, codigo_servicio, duracion, parametros_extra=None):
        try:
            cliente = self.buscar_cliente_por_nombre(nombre_cliente)
            if not cliente:
                raise ReservaInvalidaError(f"Cliente no encontrado: {nombre_cliente}")
            servicio = self.buscar_servicio_por_codigo(codigo_servicio)
            if not servicio:
                raise ReservaInvalidaError(f"Servicio no encontrado: {codigo_servicio}")
            
            reserva = Reserva(cliente, servicio, duracion, parametros_extra=parametros_extra)
            reserva.confirmar()
            self.reservas.append(reserva)
            logger.info(f"Reserva creada ID {reserva.get_id()} para {nombre_cliente}")
            return reserva
        except (ClienteInvalidoError, ServicioNoDisponibleError, DuracionInvalidaError, ReservaInvalidaError, CapacidadExcedidaError) as e:
            logger.error(f"Error crear reserva: {e}")
            logger.debug(traceback.format_exc())
            raise
        except Exception as e:
            logger.critical(f"Error inesperado: {e}")
            logger.debug(traceback.format_exc())
            raise
    
    def cancelar_reserva(self, id_reserva):
        try:
            reserva = self.buscar_reserva_por_id(id_reserva)
            if not reserva:
                raise ReservaInvalidaError(f"Reserva ID {id_reserva} no existe")
            reserva.cancelar()
            logger.info(f"Reserva {id_reserva} cancelada")
        except ReservaInvalidaError as e:
            logger.error(f"Error cancelar: {e}")
            raise
    
    def procesar_reserva(self, id_reserva):
        try:
            reserva = self.buscar_reserva_por_id(id_reserva)
            if not reserva:
                raise ReservaInvalidaError(f"Reserva ID {id_reserva} no existe")
            reserva.procesar()
            logger.info(f"Reserva {id_reserva} procesada")
        except ReservaInvalidaError as e:
            logger.error(f"Error procesar: {e}")
            raise
    
    def buscar_reserva_por_id(self, id_reserva):
        for r in self.reservas:
            if r.get_id() == id_reserva:
                return r
        return None
    
    def listar_reservas(self):
        return self.reservas.copy()
    
    def mostrar_estadisticas(self):
        logger.info(f"Total clientes: {len(self.clientes)}")
        logger.info(f"Total servicios: {len(self.servicios)}")
        logger.info(f"Total reservas: {len(self.reservas)}")
        confirmadas = sum(1 for r in self.reservas if r.get_estado() == "CONFIRMADA")
        canceladas = sum(1 for r in self.reservas if r.get_estado() == "CANCELADA")
        completadas = sum(1 for r in self.reservas if r.get_estado() == "COMPLETADA")
        logger.info(f"Reservas: Confirmadas={confirmadas}, Canceladas={canceladas}, Completadas={completadas}")
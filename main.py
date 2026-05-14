from sistema import SistemaGestion
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import *
from logger_util import logger

def main():
    sistema = SistemaGestion()
    
    # 1. Agregar servicios (3 especializados)
    print("=== 1. Creación de servicios ===")
    try:
        sala = ReservaSala("S001", "Sala de conferencias", capacidad_maxima=20, costo_por_hora=50)
        equipo = AlquilerEquipo("E002", "Proyector 4K", costo_por_dia=30, requiere_deposito=True)
        asesoria = AsesoriaEspecializada("A003", "Asesoría en Python", costo_por_hora=40, nivel_experto="Senior")
        sistema.agregar_servicio(sala)
        sistema.agregar_servicio(equipo)
        sistema.agregar_servicio(asesoria)
    except Exception as e:
        logger.error(f"Error en servicios: {e}")
    
    # 2. Registrar clientes (válidos e inválidos)
    print("\n=== 2. Registro de clientes ===")
    # Válidos
    try:
        sistema.registrar_cliente("Ana Lopez", "ana@email.com", "123456789")
    except ClienteInvalidoError as e:
        logger.error(f"Fallo: {e}")
    try:
        sistema.registrar_cliente("Carlos Ruiz", "carlos@empresa.com", "987654321")
    except ClienteInvalidoError as e:
        logger.error(f"Fallo: {e}")
    # Inválidos
    try:
        sistema.registrar_cliente("Jo", "jo@mail.com", "111222333")  # nombre corto
    except ClienteInvalidoError as e:
        logger.error(f"Excepcion capturada: {e}")
    try:
        sistema.registrar_cliente("Maria Gomez", "maria@sinpunto", "555666777")  # email malo
    except ClienteInvalidoError as e:
        logger.error(f"Excepcion capturada: {e}")
    try:
        sistema.registrar_cliente("Pedro Diaz", "pedro@mail.com", "abcd1234")  # teléfono no numérico
    except ClienteInvalidoError as e:
        logger.error(f"Excepcion capturada: {e}")
    
    # 3. Crear reservas (exitosas y fallidas)
    print("\n=== 3. Creación de reservas ===")
    # Exitosa: sala 3h con 5 personas
    try:
        r1 = sistema.crear_reserva("Ana Lopez", "S001", 3, {"cantidad_personas": 5})
        print(f"Reserva exitosa: {r1}")
    except Exception as e:
        logger.error(f"Fallo r1: {e}")
    # Exitosa: alquiler con seguro
    try:
        r2 = sistema.crear_reserva("Carlos Ruiz", "E002", 2, {"seguro": True, "deposito": 100})
        print(f"Reserva exitosa: {r2}")
    except Exception as e:
        logger.error(f"Fallo r2: {e}")
    # Exitosa: asesoría 6h (descuento)
    try:
        r3 = sistema.crear_reserva("Ana Lopez", "A003", 6)
        print(f"Reserva exitosa: {r3}")
    except Exception as e:
        logger.error(f"Fallo r3: {e}")
    # Fallida: cliente inexistente
    try:
        sistema.crear_reserva("Cliente Fantasma", "S001", 2)
    except ReservaInvalidaError as e:
        logger.error(f"Reserva fallida (cliente): {e}")
    # Fallida: servicio inexistente
    try:
        sistema.crear_reserva("Ana Lopez", "S999", 1)
    except ReservaInvalidaError as e:
        logger.error(f"Reserva fallida (servicio): {e}")
    # Fallida: duración negativa
    try:
        sistema.crear_reserva("Ana Lopez", "S001", -2)
    except DuracionInvalidaError as e:
        logger.error(f"Reserva fallida (duracion): {e}")
    # Fallida: capacidad excedida (25 > 20)
    try:
        sistema.crear_reserva("Ana Lopez", "S001", 2, {"cantidad_personas": 25})
    except CapacidadExcedidaError as e:
        logger.error(f"Reserva fallida (capacidad): {e}")
    
    # 4. Cancelar una reserva
    print("\n=== 4. Cancelacion de reserva ===")
    if 'r1' in locals():
        try:
            sistema.cancelar_reserva(r1.get_id())
            print(f"Reserva {r1.get_id()} cancelada")
        except Exception as e:
            logger.error(f"Error cancelacion: {e}")
    
    # 5. Procesar una reserva confirmada
    print("\n=== 5. Procesamiento de reserva ===")
    if 'r2' in locals():
        try:
            sistema.procesar_reserva(r2.get_id())
            print(f"Reserva {r2.get_id()} completada")
        except Exception as e:
            logger.error(f"Error procesamiento: {e}")
    
    # 6. Intentar procesar una reserva cancelada (debe fallar)
    print("\n=== 6. Intento de procesar reserva cancelada ===")
    if 'r1' in locals():
        try:
            sistema.procesar_reserva(r1.get_id())
        except ReservaInvalidaError as e:
            logger.error(f"Error esperado: {e}")
    
    # 7. Listar todas las reservas
    print("\n=== 7. Listado de reservas ===")
    for r in sistema.listar_reservas():
        print(r)
    
    # 8. Estadísticas finales
    print("\n=== 8. Estadisticas ===")
    sistema.mostrar_estadisticas()
    
    print("\n✅ Demostracion completada. Revisa 'sistema.log' para detalles de errores.")

if __name__ == "__main__":
    main()
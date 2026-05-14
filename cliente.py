import re
from excepciones import ClienteInvalidoError

class Cliente:
    def __init__(self, nombre, email, telefono):
        self._nombre = None
        self._email = None
        self._telefono = None
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_telefono(telefono)
    
    def set_nombre(self, nombre):
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: '{nombre}'. Debe tener al menos 3 caracteres.")
        self._nombre = nombre.strip()
    
    def set_email(self, email):
        # Validación simple de email
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, email):
            raise ClienteInvalidoError(f"Email inválido: '{email}'")
        self._email = email.strip()
    
    def set_telefono(self, telefono):
        if not telefono or not str(telefono).isdigit() or len(str(telefono)) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido: '{telefono}'. Debe ser numérico y tener al menos 7 dígitos.")
        self._telefono = str(telefono)
    
    # Getters
    def get_nombre(self):
        return self._nombre
    
    def get_email(self):
        return self._email
    
    def get_telefono(self):
        return self._telefono
    
    def __str__(self):
        return f"Cliente: {self._nombre}, Email: {self._email}, Tel: {self._telefono}"
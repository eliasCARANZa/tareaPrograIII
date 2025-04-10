class Cola:
    def __init__(self, tope=None):
        self._datos = []
        self._tope = tope

    def agregar(self, elemento):
        if self._tope is None or len(self._datos) < self._tope:
            self._datos.append(elemento)
        else:
            raise Exception("Capacidad de la cola alcanzada")

    def quitar(self):
        if not self.esta_vacia():
            return self._datos.pop(0)
        raise Exception("Cola vacía")

    def primero(self):
        if not self.esta_vacia():
            return self._datos[0]
        return None

    def esta_vacia(self):
        return len(self._datos) == 0

    def largo(self):
        return len(self._datos)

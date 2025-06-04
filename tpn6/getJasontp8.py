"""
Sistema de Pagos - Versión 1.2

Este programa automatiza el proceso de selección de cuenta bancaria para pagos,
utilizando patrones de diseño como Singleton, Cadena de Responsabilidad e Iterador.
"""

import json


class TokenManager:
    """Singleton que gestiona claves de bancos desde un archivo JSON."""

    _instance = None

    def __new__(cls, json_file='sitedata.json'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open(json_file, 'r', encoding='utf-8') as file:
                cls._instance.tokens = json.load(file)
        return cls._instance

    def get_key(self, token):
        """Devuelve la clave asociada al token."""
        return self.tokens.get(token)


class Cuenta:
    """Representa una cuenta bancaria."""

    def __init__(self, token, saldo_inicial):
        self.token = token
        self.saldo = saldo_inicial
        self.historial = []

    def pagar(self, pedido_id, monto):
        """
        Intenta realizar un pago.

        Retorna True si el pago fue exitoso, False si no hay saldo suficiente.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            self.historial.append((pedido_id, monto))
            return True
        return False


class ManejadorPago:
    """
    Nodo en la cadena de responsabilidad para procesar pagos.

    Intenta pagar con su cuenta, y si no puede, pasa al siguiente nodo.
    """

    def __init__(self, cuenta, siguiente=None):
        self.cuenta = cuenta
        self.siguiente = siguiente

    def manejar(self, pedido_id, monto):
        """Procesa el pago con esta cuenta o la siguiente en la cadena."""
        if self.cuenta.pagar(pedido_id, monto):
            clave = TokenManager().get_key(self.cuenta.token)
            return {
                'pedido': pedido_id,
                'token': self.cuenta.token,
                'clave': clave,
                'monto': monto
            }
        if self.siguiente:
            return self.siguiente.manejar(pedido_id, monto)
        return {'pedido': pedido_id, 'error': 'Fondos insuficientes'}


class SistemaPagos:
    """
    Controlador del sistema de pagos.

    Encapsula las cuentas, historial de pagos y el ruteo automático.
    """

    def __init__(self):
        self.cuenta1 = Cuenta('token1', 1000)
        self.cuenta2 = Cuenta('token2', 2000)
        self.chain = ManejadorPago(self.cuenta1, ManejadorPago(self.cuenta2))
        self.historial = []

    def solicitar_pago(self, pedido_id, monto):
        """Solicita un pago, se registra si fue exitoso."""
        resultado = self.chain.manejar(pedido_id, monto)
        if 'error' not in resultado:
            self.historial.append(resultado)
        return resultado

    def listar_pagos(self):
        """Itera y muestra los pagos realizados en orden cronológico."""
        for pago in self.historial:
            print(pago)


VERSION = '1.2'


def main():
    """Función principal para ejecutar la simulación de pagos."""
    print(f"Sistema de Pagos - Versión {VERSION}")
    sistema = SistemaPagos()

    pedidos = [(1, 500), (2, 500), (3, 500), (4, 500), (5, 500), (6, 500)]
    for pedido_id, monto in pedidos:
        resultado = sistema.solicitar_pago(pedido_id, monto)
        print(resultado)

    print("\nHistorial de pagos:")
    sistema.listar_pagos()


if __name__ == "__main__":
    main()

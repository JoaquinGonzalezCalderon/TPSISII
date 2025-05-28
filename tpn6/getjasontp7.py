#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getJason_refactored.py - versión 1.1

Copyright UADER-FCyT-IS2©2024 - Todos los derechos reservados.

Este programa permite recuperar cualquier valor de clave presente en el archivo 'sitedata.json'.
Emplea Programación Orientada a Objetos, patrón de diseño Singleton, y una estrategia
"Branching by Abstraction" para converger con la versión funcional previa.

Uso:
    python getJason_refactored.py [clave]
    python getJason_refactored.py -v       # Muestra la versión del programa
"""

import json
import sys
import os


class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton.
    Asegura que la clase sólo tenga una única instancia.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instancia = super().__call__(*args, **kwargs)
            cls._instances[cls] = instancia
        return cls._instances[cls]


class JsonLoader(metaclass=SingletonMeta):
    """
    Clase Singleton responsable de leer y buscar claves en un archivo JSON.
    """
    def __init__(self, filename="sitedata.json"):
        self.filename = filename
        self.data = None

    def load_json(self):
        """Carga el archivo JSON."""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Archivo '{self.filename}' no encontrado.")
        with open(self.filename, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get_value(self, key):
        """Devuelve el valor de la clave solicitada."""
        if self.data is None:
            raise ValueError("El JSON no ha sido cargado.")
        if key not in self.data:
            raise KeyError(f"Clave '{key}' no encontrada en el archivo.")
        return self.data[key]


def legacy_main():
    """
    Versión original funcional - punto de partida para "Branching by abstraction".
    """
    key = sys.argv[1] if len(sys.argv) > 1 else "token1"

    try:
        with open("sitedata.json", "r") as file:
            data = json.load(file)

        if key in data:
            print(data[key])
        else:
            print(f"Clave '{key}' no encontrada en el archivo.")
    except FileNotFoundError:
        print("Error: El archivo 'sitedata.json' no fue encontrado.")
    except json.JSONDecodeError:
        print("Error: El archivo 'sitedata.json' no contiene un JSON válido.")


def main():
    """
    Punto de entrada principal de la nueva versión orientada a objetos.
    Realiza chequeos robustos y captura errores de forma controlada.
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "-v":
            print("Versión 1.1")
            return
        key = arg
    else:
        key = "token1"

    try:
        loader = JsonLoader()
        loader.load_json()
        value = loader.get_value(key)
        print(value)
    except FileNotFoundError as fnf:
        print(f"Error: {fnf}")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{loader.filename}' no contiene un JSON válido.")
    except KeyError as ke:
        print(f"Error: {ke}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()

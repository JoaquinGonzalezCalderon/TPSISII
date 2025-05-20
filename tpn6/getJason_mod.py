# getJason_mod.py
# Este script permite recuperar cualquier valor de clave presente en sitedata.json
# Uso: python getJason_mod.py [clave]
# Si no se especifica ninguna clave, se utiliza "token1" por defecto.

import json
import sys

def main():
    # Obtener la clave desde los argumentos o usar "token1" por defecto
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

if __name__ == "__main__":
    main()

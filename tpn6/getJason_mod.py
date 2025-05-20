# getJason_mod.py
import json
import sys

def main():
    # Clave por defecto
    key = sys.argv[1] if len(sys.argv) > 1 else "token1"

    # Leer archivo JSON
    with open("sitedata.json", "r") as f:
        data = json.load(f)

    # Mostrar resultado
    if key in data:
        print(data[key])
    else:
        print(f"Clave '{key}' no encontrada.")

if __name__ == "__main__":
    main()

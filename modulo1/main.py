import json
import logging
import re

logging.basicConfig(
    filename="errores.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def process_user(usuario):
    # pattern matching para verificar el ROL
    match usuario.get("rol"):
        case "admin":
            return "Prioridad alta"
        case "editor":
            return "Prioridad media"
        case _:
            return "Prioridad baja"


def validate_email(email):
    # expresión regular simple para validar email
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if email and re.match(patron, email):
        return True
    return False


def main():
    try:
        with open("datos.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo datos.json")
        return
    except json.JSONDecodeError:
        print("Error: El formato del JSON es inválido")
        return

    resultados = []

    for user in usuarios:
        try:
            if not isinstance(user.get("id"), int):
                raise ValueError(f"ID invalido para el usuario: {user.get('nombre')}")

            if not validate_email(user.get("email")):
                logging.warning(f"Email invalido para ID {user.get('id')}")

            user["prioridad"] = process_user(user)
            user["procesado"] = True
            resultados.append(user)

        except Exception as e:
            logging.error(f"Error procesando registro: {e}")
            print("Error en un registro. Revisar errores.log")
            continue

    with open("procesados.json", "w") as f:
        json.dump(resultados, f, indent=4)
    print("Proceso terminado. Revisa procesados.json y errores.log")


if __name__ == "__main__":
    main()

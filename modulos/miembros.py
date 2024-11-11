"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
from termcolor import colored
import regex as re
import modulos.tools as tul

def crear_miembro() -> None:
    """
    Esta función permite crear un nuevo miembro y agrega registros tanto a
    miembros.csv como member_data.json.
    No recibe ni retorna nada.
    """
    patron_mail = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    names = tul.read_csv(r"data/miembros.csv")
    miembros = tul.read_json(r"data/member_data.json")
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("CARGA DE MIEMBROS","yellow"))

        nombre = input("Ingrese el nombre del miembro (ENTER para salir): ")

        if nombre:
            while True:
                print("Ingrese la dirección de correo electrónico asociada a este miembro:")
                email = input()
                if re.match(patron_mail, email):
                    #lo cargo en el csv
                    idgen = int(list(names.keys())[-1]) + 1
                    names[str(idgen)] = {
                        'NOMBRE': nombre,
                        'EMAIL': email
                    }
                    tul.write_csv('data/miembros.csv', names)
                    #lo cargo en el json
                    miembros[str(idgen)] = {
                        "status": 1,
                        "roles": [],
                        "grupos_de_trabajo": [],
                        "tareas_asignadas": [],
                        "historial": []
                    }
                    tul.write_json('data/member_data.json', miembros)
                    print(colored("Miembro cargado correctamente.", "green"))
                    sleep(1.5)
                else:
                    print(colored(
                        "La dirección de correo electrónico no es válida. Intente nuevamente.","red"
                    )
                    )
                    sleep(1.5)
                break
        else:
            print(colored("Operación cancelada. Saliendo...", "red"))
            sleep(1)
            break


def gestion_miembros() -> None:
    """
    Esta función muestra las opciones del submenú de gestión de miembros y
    permite al usuario interactuar con el programa.
    """

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("GESTIÓN DE MIEMBROS", "green"))
        opciones = [
            "Cargar un miembro",
            "Eliminar un miembro",
            "Buscar un miembro",
            "Volver",
        ]
        tul.show_options(opciones)

        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)
        else:
            match user_input:
                case 1:
                    crear_miembro()
                case 2:
                    eliminar_miembro()
                case 3:
                    buscar_miembro()
                case 4:
                    print(colored("Volviendo al menú principal...", "red"))
                    sleep(1.5)
                    break
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)

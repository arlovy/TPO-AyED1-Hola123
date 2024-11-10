"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
import modulos.tools as tul
from termcolor import colored

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
                    cargar_miembro()
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

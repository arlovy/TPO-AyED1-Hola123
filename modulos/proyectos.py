"""
Este modulo inicializa la secuencia de gestion de proyectos.
"""

from time import sleep
import modulos.tools as tul
from termcolor import colored


def ver_proyectos() -> None:
    """
    Esta función permite al usuario visualizar todos los proyectos.
    Además debe permitir acceder a cada uno en detalle y gestionarlos.
    """


def crear_proyecto() -> None:
    """
    Esta función permite al usuario crear nuevos proyectos en el archivo JSON
    de proyectos.
    """


def gestion_proyectos() -> None:
    """
    Esta función muestra las opciones del submenú de gestión de miembros y
    permite al usuario interactuar con el programa.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("GESTIÓN DE PROYECTOS", "yellow"))
        opciones = [
            "Ver proyectos",
            "Crear un proyecto",
            "Volver",
        ]
        tul.show_options(opciones)

        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                ver_proyectos()
            case 2:
                crear_proyecto()
            case 3:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)

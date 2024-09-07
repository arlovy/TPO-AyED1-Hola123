"""
Este archivo contiene el código que inicializa la aplicación.
"""

from os import system, name
from time import sleep
import lib.constantes as cons
import lib.gestion_miembros as members
import lib.gestion_proyectos as projects
from tabulate import tabulate
from termcolor import colored


def limpiar_pantalla():
    """
    Esta función se encarga de limpiar la consola.
    """

    # Para Windows
    if name == "nt":
        _ = system("cls")

    # Para Mac y Linux
    else:
        _ = system("clear")


def show_options(options: list[str]):
    """
    Esta función recibe una lista de strings y la imprime, enumerándola
    para permitir al usuario interactuar con el programa.
    """
    for opcion in enumerate(options):
        print(f"{opcion[0] + 1}. {opcion[1]}")
    print()


def printear_logo():
    """
    Esta función printea el logo de SPM usando tabulate. Trae
    el logo ASCII de SPM del archivo constantes.py
    """
    limpiar_pantalla()
    pantalla = [
        ["Software Project Manager by Hola123"],
        [cons.LOGO],
    ]  # elementos de la pantalla principal
    print(
        tabulate(pantalla, colalign=("center",))
    )  # printea pantalla principal con tabulate


def main_screen():
    """
    Esta función inicializa la pantalla principal del programa.
    """
    while True:
        limpiar_pantalla()
        printear_logo()
        opciones = [
            "Gestión de miembros",
            "Gestión de proyectos",
            "Salir",
        ]  # opciones pantalla principal
        show_options(opciones)

        try:
            user_input = int(input("Ingrese la opción: "))

            match user_input:
                case 1:
                    members.gestion_miembros()
                    continue
                case 2:
                    # projects.gestion_tareas()
                    continue
                case 3:
                    print(colored("Saliendo del programa...", "red"))
                    sleep(2)
                    limpiar_pantalla()
                    break  # rompe el while true y finaliza el programa
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)
                    continue
        except ValueError:
            print(colored("La opción ingresada no es válida.", "red"))
            sleep(1)


if __name__ == "__main__":
    main_screen()

"""
Este archivo contiene el código que inicializa la aplicación.
"""

from os import system, name
from time import sleep
import constantes as cons
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


def ver_proyectos():
    """
    Esta función permite al usuario visualizar todos los proyectos. 
    Además debe permitir acceder a cada uno en detalle y gestionarlos.
    """


def crear_proyecto():
    """
    Esta función permite al usuario crear nuevos proyectos en el archivo JSON
    de proyectos. 
    """

def gestion_proyectos():
    """
    Esta función muestra las opciones del submenú de gestión de miembros y
    permite al usuario interactuar con el programa.
    """
    while True:
        printear_logo()
        print(colored("GESTIÓN DE PROYECTOS", "yellow"))
        opciones = [
            "Ver proyectos",
            "Crear un proyecto",
            "Borrar un proyecto",
            "Volver",
        ]
        show_options(opciones)

  
        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                ver_proyectos()
            case 2:
                crear_proyecto()
            case 3:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(2)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)
                continue

def cargar_miembro():
    """
    Esta función debe acceder al archivo JSON de los miembros
    y permitir al usuario cargar uno nuevo.
    """


def eliminar_miembro():
    """
    Esta función debe permitir al usuario eliminar miembros
    del archivo JSON. Deberá solicitar una confirmación antes
    de efectuar la eliminación.
    """


def buscar_miembro():
    """
    Esta función debe permitir al usuario buscar miembros en el
    archivo JSON y mostrar su información.
    """


def gestion_miembros():
    """
    Esta función muestra las opciones del submenú de gestión de miembros y
    permite al usuario interactuar con el programa.
    """

    while True:
        printear_logo()
        print(colored("GESTIÓN DE MIEMBROS", "green"))
        opciones = [
            "Cargar un miembro",
            "Eliminar un miembro",
            "Buscar un miembro",
            "Volver",
        ]
        show_options(opciones)

        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                cargar_miembro()
            case 2:
                eliminar_miembro()
            case 3:
                buscar_miembro()
            case 4:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(2)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)
                continue


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
                    gestion_miembros()
                    continue
                case 2:
                    gestion_proyectos()
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
            print(colored("Elija una opción numérica.", "red"))
            sleep(1)


if __name__ == "__main__":
    main_screen()

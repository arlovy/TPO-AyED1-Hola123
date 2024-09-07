"""
Este modulo inicializa el programa para la gestión de miembros.
"""

from time import sleep
from aplicacion import printear_logo, show_options
from termcolor import colored


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
    printear_logo()
    print(colored("GESTIÓN DE MIEMBROS", "green"))
    opciones = [
        "Cargar un miembro",
        "Eliminar un miembro",
        "Buscar un miembro",
        "Volver",
    ]
    show_options(opciones)

    while True:
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

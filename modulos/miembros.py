"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
import csv
import modulos.tools as tul
from termcolor import colored


def cargar_miembro():
    """
    Esta función debe acceder al archivo JSON de los miembros
    y permitir al usuario cargar uno nuevo.
    """


def eliminar_miembro():
    """
    Esta función debe permitir al usuario dar de baja miembros
    del archivo CSV. Deberá solicitar una confirmación antes
    de efectuar la eliminación. Al dar de baja, la especialidad
    en el CSV se establece en -1.
    """


def buscar_miembro():
    """
    Esta función debe permitir al usuario buscar miembros en el
    archivo CSV y mostrar su información.
    Debe permitir buscar por varias categorías.
    """
    


def gestion_miembros():
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
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)

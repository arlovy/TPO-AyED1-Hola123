"""
Este módulo contiene funciones que son utilizadas por todo el programa.
"""

from os import system, name
from tabulate import tabulate
import modulos.constantes as cons

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
    for numero, opcion in enumerate(options):
        print(f"{numero + 1}. {opcion}")
    print()

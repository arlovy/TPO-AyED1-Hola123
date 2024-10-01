"""
Este módulo contiene funciones que son utilizadas por todo el programa.
"""

from os import system, name
from tabulate import tabulate
import modulos.constantes as cons

def printear_logo() -> None:
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


def limpiar_pantalla() -> None:
    """
    Esta función se encarga de limpiar la consola.
    """

    # Para Windows
    if name == "nt":
        _ = system("cls")

    # Para Mac y Linux
    else:
        _ = system("clear")


def show_options(options: list[str]) -> None:
    """
    Esta función recibe una lista de strings y la imprime, enumerándola
    para permitir al usuario interactuar con el programa.
    """
    for numero, opcion in enumerate(options):
        print(f"{numero + 1}. {opcion}")
    print()

def abrir_csv(ruta_csv: str) -> list[list[str]]:
    """
    Esta función genera una matriz a partir de un archivo CSV para ser trabajada.
    Recibe como parámetro un string con la ruta del archivo CSV a leer.
    Retorna una lista de listas donde cada índice representa una fila del CSV.
    """
    with open(ruta_csv, "r", encoding="utf-8") as csvfile:
        archivocsv = list(map(lambda x: x.split(","),csvfile.readlines()))
        for lista in archivocsv:
            lista[3] = lista[3].replace("\n", "")
    return archivocsv

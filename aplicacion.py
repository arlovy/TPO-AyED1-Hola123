import constantes as cons
from tabulate import tabulate
from os import system, name
from time import sleep
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


def main_screen():
    """
    Esta función inicializa la pantalla principal del programa.
    """
    limpiar_pantalla()
    main_screen = [
        ["Software Project Manager by Hola123"],
        [cons.logo],
    ]  # elementos de la pantalla principal
    print(
        tabulate(main_screen, colalign=("center",))
    )  # printea pantalla principal con tabulate

    opciones = [
        "Gestión de miembros",
        "Gestión de tareas",
        "Salir",
    ]  # opciones pantalla principal
    show_options(opciones)

    while True:
        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                gestion_miembros()
            case 2:
                gestion_tareas()
            case 3:
                limpiar_pantalla()
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(2)
                main_screen()
                break


if __name__ == "__main__":
    main_screen()

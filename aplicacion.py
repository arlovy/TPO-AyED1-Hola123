"""
Este archivo contiene el código que inicializa la aplicación.
"""

from time import sleep
import modulos.tools as tul
from termcolor import colored
import modulos.miembros as memb
import modulos.proyectos as proj


def main_screen() -> None:
    """
    Esta función inicializa la pantalla principal del programa.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        opciones = [
            "Gestión de miembros",
            "Gestión de proyectos",
            "Salir",
        ]  # opciones pantalla principal
        tul.show_options(opciones)
        print(tul.abrir_csv("data/members.csv"))
        try:
            user_input = int(input("Ingrese la opción: "))

            match user_input:
                case 1:
                    memb.gestion_miembros()
                case 2:
                    proj.gestion_proyectos()
                case 3:
                    print(colored("Saliendo del programa...", "red"))
                    sleep(1.5)
                    tul.limpiar_pantalla()
                    break  # rompe el while true y finaliza el programa
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)
                    continue
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)


if __name__ == "__main__":
    main_screen()

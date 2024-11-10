"""
Este archivo contiene el código que inicializa la aplicación.
"""

from time import sleep
import modulos.tools as tul
from termcolor import colored
import modulos.miembros as memb
import modulos.proyectos as proj
import modulos.panel as pan


def main_screen() -> None:
    """
    Esta función inicializa la pantalla principal del programa.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        opciones = [
            "Panel de control",
            "Gestionar proyectos",
            "Gestion de miembros",
            "Salir",
        ]  # opciones pantalla principal
        tul.show_options(opciones)
        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)
        else:
            match user_input:
                case 1:
                    pan.panel()
                case 2:
                    proj.gestion_proyectos()
                case 3:
                    memb.gestion_miembros()
                case 4:
                    print(colored("Saliendo del programa...", "red"))
                    sleep(1.5)
                    tul.limpiar_pantalla()
                    break  # rompe el while true y finaliza el programa
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)
                    continue


if __name__ == "__main__":
    try:
        main_screen()

    #la combinacion ctrl + c termina forzadamente el programa, este try atrapa ese caso
    except KeyboardInterrupt:
        print()
        print(colored("Error. Se ha interrumpido el programa a través del teclado.", "red"))
        print(colored("Saliendo del programa...", "red"))
        sleep(1.5)
        tul.limpiar_pantalla()

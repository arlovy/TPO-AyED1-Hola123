"""
Este modulo inicializa la secuencia de gestion de proyectos.
"""

from time import sleep
from termcolor import colored
import modulos.tools as tul

def crear_proyecto() -> None:
    """
    Permite generar un nuevo proyecto.
    No retorna ni recibe nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")
    groupnames = tul.read_csv(r"data/proyectos.csv")

    tul.limpiar_pantalla()
    tul.printear_logo()

    print(colored("CREAR PROYECTO", "light_green"))
    while True:
        nombre = input("Ingrese el nombre del proyecto (-1 para cancelar): ")
        if nombre == "-1" or nombre in [""," "]:
            print(colored("Saliendo...", "red"))
            sleep(1.3)
            break
        else:
            print("Ingrese una descripción para el proyecto: ")
            desc = input()
            if proyectos:
                id_ = list(proyectos.keys())[-1]
            else:
                id_ = "100" #las ids de proyectos empiezan en 100

            proyectos[id_] = {
                "status": 2,
                "descripcion": desc,
                "fecha_inicio": "",
                "fecha_fin": "",
                "miembros_asignados": [],
                "leader": 0,
                "tareas": []
            }

            groupnames[id_] = {
                "NOMBRE DE PROYECTO": nombre
            }
            tul.write_csv(r"data/proyectos.csv", groupnames)
            tul.write_json(r"data/project_data.json", proyectos)
            print(colored("Proyecto generado exitosamente.", "green"))
            sleep(1.3)
            break


def ver_proyectos() -> None:
    pass


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
            "Crear un proyecto",
            "Ver proyectos",
            "Volver",
        ]
        tul.show_options(opciones)

        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                crear_proyecto()
            case 2:
                ver_proyectos()
            case 3:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)

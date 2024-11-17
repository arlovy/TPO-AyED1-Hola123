"""
Este modulo inicializa la secuencia de gestion de proyectos.
"""

from time import sleep
from termcolor import colored
import modulos.tools as tul
import modulos.constantes as cons

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
                id_ = int(list(proyectos.keys())[-1]) + 1
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
    """
    Permite al usuario visualizar los proyectos cargados en el sistema.
    No recibe ni retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")
    groupnames = tul.read_csv(r"data/proyectos.csv")
    names = tul.read_csv(r"data/miembros.csv")
    indent = "    "

    tul.limpiar_pantalla()
    tul.printear_logo()

    print(colored("GRUPOS CARGADOS", "light_green"))
    if not groupnames:
        print(colored("No hay proyectos cargados en el sistema."))
    else:
        for id_, item in groupnames.items():
            print(colored(f"PROYECTO {id_} - {item['NOMBRE DE PROYECTO']}", "yellow"))

            print(
                colored(
                    f"ESTADO: {cons.project_status.get(proyectos[id_]['status'])}", "dark_grey"
                )
            )

            print(colored("MIEMBROS:", "dark_grey"))
            if proyectos[id_]['miembros_asignados']:
                for miembro in proyectos[id_]['miembros_asignados']:
                    print(indent + colored(f"‣{names[str(miembro)]['NOMBRE']}", "dark_grey"))
            else:
                print(indent + colored("Este grupo no tiene miembros asignados.", "dark_grey"))
            print("⸻⸻⸻" * 5) #un separador para que sea mas facil de leer
    print(colored("Presione ENTER para volver.", "yellow"))
    input()


def project_status(id_:str) -> None:
    """
    Permite al usuario editar el estado de un proyecto indicado.
    Recibe una ID en forma de string.
    No retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("EDITAR ESTADO", "yellow"))
        print(
            colored(
                f"ESTADO ACTUAL: {cons.project_status.get(proyectos[id_]['status'])}", "dark_grey"
            )
        )
        tul.show_options(cons.project_status.values())

        try:
            estado_input = int(input("Ingrese el estado deseado (-1 para cancelar): "))
        except ValueError:
            print(colored("Ingrese un valor válido.", "red"))
            sleep(1.3)
        else:
            if estado_input == -1:
                print(colored("Volviendo...", "red"))
                sleep(1.3)
                break
            elif estado_input not in [1,2,3]:
                print(colored("Opción no válida.", "red"))
                sleep(1.3)
            else:
                proyectos[id_]['status'] = estado_input
                tul.write_json(r"data/project_data.json", proyectos)


def manage_members(id_:str) -> None:
    """
    Permite al usuario eliminar miembros del grupo indicado.
    Recibe una ID en forma de string.
    No retorna nada.
    """
    names = tul.read_csv(r"data/miembros.csv")
    proyectos = tul.read_json(r"data/project_data.json")
    miembros = tul.read_json(r"data/member_data.json")
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("ELIMINAR MIEMBROS", "yellow"))
        if not proyectos[id_]['miembros_asignados']:
            print(colored("No hay miembros asignados al proyecto.", "dark_grey"))
            print(colored("ENTER para volver.", "dark_grey"))
            input()
            break
        else:
            for miembro in proyectos[id_]['miembros_asignados']:
                print(f"{miembro} - {names[str(miembro)]['NOMBRE']}")
            try:
                user_input = int(input("Ingrese la ID del usuario a eliminar (-1 para cancelar): "))
            except ValueError:
                print(colored("Ingrese un valor válido.", "red"))
                sleep(1.5)
            else:
                if user_input == -1:
                    print(colored("Volviendo...", "red"))
                    sleep(1.3)
                    break
                elif user_input not in proyectos[id_]['miembros_asignados']:
                    print(colored("El miembro indicado no existe.", "dark_grey"))
                    sleep(1.3)
                else:
                    proyectos[id_]['miembros_asignados'].remove(user_input)
                    miembros[str(user_input)]['grupos_de_trabajo'].remove(int(id_))
                    tul.write_json(r"data/project_data.json", proyectos)
                    tul.write_json(r"data/member_data.json", miembros)
                    print(colored("Operación exitosa.", "green"))
                    sleep(1.3)


def set_leader(id_: str) -> None:
    """
    Permite al usuario asignar un lider a un grupo de trabajo indicado, eligiendo entre
    sus miembros actuales.
    Recibe una ID en formato string.
    No retorna nada.
    """
    names = tul.read_csv(r"data/miembros.csv")
    proyectos = tul.read_json(r"data/project_data.json")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("DEFINIR LIDER DE EQUIPO", "yellow"))
        if not proyectos[id_]['miembros_asignados']:
            print(colored("No hay miembros asignados al proyecto.", "dark_grey"))
            print(colored("ENTER para volver.", "dark_grey"))
            input()
            break
        else:
            for miembro in proyectos[id_]['miembros_asignados']:
                nombre = names[str(miembro)]['NOMBRE']
                if miembro == proyectos[id_]['leader']:
                    print(f"{miembro} - {nombre} " + colored("LIDER", "green"))
                else:
                    print(f"{miembro} - {nombre}")
            try:
                user_input = int(input("Ingrese la ID del nuevo lider (-1 para cancelar): "))
            except ValueError:
                print(colored("ID no válida.", "red"))
                sleep(1.5)
                continue

            if user_input == -1:
                print(colored("Volviendo...", "red"))
                sleep(1.3)
                break
            elif user_input not in proyectos[id_]['miembros_asignados']:
                print(colored("Miembro no válido.", "dark_grey"))
                sleep(1.3)
                continue
            elif user_input == proyectos[id_]['leader']:
                print(colored("Este miembro ya es el líder del equipo.", "dark_grey"))
                sleep(1.3)
                continue
            else:
                proyectos[id_]['leader'] = user_input
                tul.write_json(r"data/project_data.json", proyectos)
                print(colored("Operación exitosa.", "green"))
                sleep(1.3)



def edit_project_instance(id_:str) -> None:
    """
    Permite al usuario acceder a las opciones de edición de un proyecto indicado.
    Recibe un ID en forma de string.
    No retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")
    groupnames = tul.read_csv(r"data/proyectos.csv")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored(f"EDITANDO PROYECTO: {groupnames[id_]['NOMBRE DE PROYECTO']}", "yellow"))
        descripcion = proyectos[id_]['descripcion']
        print(colored(f'"{descripcion}"', "dark_grey"))
        print("⸻⸻⸻" * 5)

        opciones = [
            "Editar estado del proyecto",
            "Eliminar miembros",
            "Definir lider del equipo",
            "Administrar tareas",
            "Volver"
        ]

        tul.show_options(opciones)
        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)
            continue

        match user_input:
            case 1:
                project_status(id_)
            case 2:
                manage_members(id_)
            case 3:
                set_leader(id_)
            case 4:
                manage_tasks()
            case 5:
                print(colored("Volviendo...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)


def manage_projects() -> None:
    """
    Esta función iniciliza la secuencia de administración de proyectos.
    No recibe ni retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored("ADMINISTRACIÓN DE PROYECTOS", "magenta"))
        id_proyecto = input("Ingrese la ID del proyecto que desea gestionar (-1 para cancelar): ")

        if id_proyecto == "-1" or id_proyecto in ["", " "]:
            print(colored("Acción cancelada. Volviendo...", "red"))
            sleep(1.3)
            break

        if id_proyecto not in proyectos:
            print(colored("El proyecto indicado no existe.", "dark_grey"))
            sleep(1.3)
        else:
            edit_project_instance(id_proyecto)


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
            "Administrar un proyecto",
            "Volver",
        ]
        tul.show_options(opciones)

        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)

        match user_input:
            case 1:
                crear_proyecto()
            case 2:
                ver_proyectos()
            case 3:
                manage_projects()
            case 4:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)

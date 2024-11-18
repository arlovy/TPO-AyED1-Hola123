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
        print(colored("No hay proyectos cargados en el sistema.", "dark_grey"))
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
                if estado_input == 1 and not proyectos[id_]['fecha_inicio']:
                    proyectos[id_]['fecha_inicio'] = tul.get_date()
                elif estado_input == 3 and not proyectos[id_]['fecha_fin']:
                    proyectos[id_]['fecha_fin'] = tul.get_date()
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


def see_tasks(id_:str) -> None:
    """
    Muestra las tareas dentro de un proyecto indicado.
    Recibe una ID de proyecto en forma de string.
    No retorna nada.
    """
    tasks = tul.read_json(r"data/tasks.json")
    proyectos = tul.read_json(r"data/project_data.json")
    names = tul.read_csv(r"data/miembros.csv")
    indent = "    "

    tul.limpiar_pantalla()

    if not proyectos[id_]['tareas']:
        print(colored("No hay tareas en este proyecto.", "dark_grey"))
    else:
        print(colored("TAREAS", "yellow"))
        for task_id in proyectos[id_]['tareas']:
            print(colored(f"ID:{task_id} - {tasks[str(task_id)]['nombre_tarea']}", "dark_grey"))

            descripcion = tasks[str(task_id)]['descripcion']
            print(indent + colored(f'"{descripcion}"', "dark_grey"))

            print(indent +
                  colored(
                    f"ESTADO: {cons.task_status.get(tasks[str(task_id)]['status'])}", "dark_grey"
                )
            )

            print(indent + colored("MIEMBROS:", "dark_grey"))
            if not tasks[str(task_id)]['asignado_a']:
                print(indent + colored("No hay miembros asignados a esta tarea.", "dark_grey"))
            else:
                for id_miembro, datos in names.items():
                    if int(id_miembro) in tasks[str(task_id)]['asignado_a']:
                        print(indent + colored(f"ID:{id_miembro} - {datos['NOMBRE']}", "dark_grey"))

            print(colored("⸻⸻⸻" * 5, "dark_grey"))
    print(colored("ENTER para salir.", "yellow"))
    input()


def add_tasks(id_:str) -> None:
    """
    Permite al usuario cargar una tarea dentro de un proyecto.
    Recibe la ID del proyecto en forma de string.
    No retorna nada.
    """
    tasks = tul.read_json(r"data/tasks.json")
    proyectos = tul.read_json(r"data/project_data.json")

    while True:
        tul.limpiar_pantalla()
        print(colored("CREAR TAREA", "yellow"))
        nombre = input("Ingrese el nombre de la tarea (-1 para cancelar): ")
        if nombre == "-1" or nombre in [""," "]:
            print(colored("Saliendo...", "red"))
            sleep(1.3)
            break
        else:
            print("Ingrese una descripción para la tarea: ")
            desc = input()
            if not tasks:
                task_id = "200"
            else:
                task_id = str(int(list(tasks.keys())[-1]) + 1)

            tasks[task_id] = {
                "nombre_tarea": nombre,
                "descripcion": desc,
                "status": 1,
                "fecha_inicio": "",
                "fecha_fin": "",
                "asignado_a": [],
                "proyecto": int(id_)
            }
            proyectos[id_]['tareas'].append(int(task_id))
            tul.write_json(r"data/project_data.json", proyectos)
            tul.write_json(r"data/tasks.json", tasks)
            print(colored("Tarea cargada correctamente", "green"))
            sleep(1.3)


def edit_task_status(id_:str) -> None:
    """
    Permite al usuario editar el estatus de una tarea dentro de un proyecto.
    Recibe la ID del proyecto en forma de string.
    No retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")
    tasks = tul.read_json(r"data/tasks.json")
    miembros = tul.read_json(r"data/member_data.json")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("EDITAR ESTADO", "yellow"))
        if not proyectos[id_]['tareas']:
            print(colored("No hay tareas en este equipo.", "dark_grey"))
            print(colored("Presione ENTER para volver.", "dark_grey"))
            input()
            break

        for tarea in proyectos[id_]['tareas']:
            print(f"{tarea} - {tasks[str(tarea)]['nombre_tarea']}")
        print()

        try:
            task_input = int(input("Ingrese la ID de la tarea (-1 para cancelar): "))
        except ValueError:
            print(colored("ID no válida.", "red"))
            sleep(1.5)
            continue

        if task_input == -1:
            print(colored("Volviendo...", "red"))
            sleep(1.3)
            break

        if task_input not in proyectos[id_]['tareas']:
            print(colored("Esta tarea no existe en este proyecto.", "dark_grey"))
            sleep(1.3)
        else:
            for val, text in cons.task_status.items():
                print(f"{val} - {text}")

            try:
                user_input = int(input("Ingrese el estado nuevo: "))
                if user_input not in [1,2,3]:
                    raise ValueError
            except ValueError:
                print(colored("Estado no válido.", "red"))
                sleep(1.5)
                continue

            tasks[str(task_input)]['status'] = user_input
            if user_input == 2 and not tasks[str(task_input)]['fecha_inicio']:
                tasks[str(task_input)]['fecha_inicio'] = tul.get_date()
            elif user_input == 3 and not tasks[str(task_input)]['fecha_fin']:
                tasks[str(task_input)]['fecha_fin'] = tul.get_date()
                for miembro in tasks[str(task_input)]['asignado_a']:
                    miembros[str(miembro)]['historial'].append(task_input)

            tul.write_json(r"data/tasks.json", tasks)
            print(colored("Operación exitosa.", "green"))
            sleep(1.3)
            break


def manage_task_members(id_: str, task_id: int) -> None:
    """
    Permite al usuario administrar los miembros de una tarea.
    Recibe la ID del proyecto en forma de string, y la ID de la tarea en forma de entero.
    No retorna nada.
    """
    miembros = tul.read_json(r"data/member_data.json")
    proyectos = tul.read_json(r"data/project_data.json")
    names = tul.read_csv(r"data/miembros.csv")
    tareas = tul.read_json(r"data/tasks.json")
    while True:
        tul.limpiar_pantalla()

        print()
        print(colored(f"EDITANDO TAREA: {tareas[str(task_id)]['nombre_tarea']}", "yellow"))
        for members in proyectos[id_]['miembros_asignados']:
            if members not in tareas[str(task_id)]['asignado_a']:
                sufijo = ""
            else:
                sufijo = colored(" ASIGNADO", "green")
            print(f"{members} - {names[str(members)]['NOMBRE']}" + sufijo)
        print("⸻⸻⸻" * 5)

        try:
            user_input = int(input("Ingrese la ID del miembro a modificar (-1 para cancelar): "))
            if user_input not in proyectos[id_]['miembros_asignados'] and user_input != -1:
                raise ValueError
        except ValueError:
            print(colored("ID no válida.", "red"))
            sleep(1.5)
            continue

        if user_input == -1:
            print(colored("Volviendo...", "red"))
            sleep(1.3)
            break

        choice_input = input(
            "¿Desea agregar o eliminar a este miembro? (1 - AGREGAR / 0 - ELIMINAR): "
        )

        if choice_input not in ["1","0"]:
            print("Opción no válida.", "red")
            sleep(1.3)
            continue
        elif choice_input == "1":
            if user_input in tareas[str(task_id)]['asignado_a']:
                print("Este miembro ya está anotado en esta tarea.", "dark_grey")
            else:
                tareas[str(task_id)]['asignado_a'].append(user_input)
                miembros[str(user_input)]['tareas_asignadas'].append(task_id)
                tul.write_json(r"data/tasks.json", tareas)
                tul.write_json(r"data/member_data.json", miembros)
        elif choice_input == "0":
            if user_input not in tareas[str(task_id)]['asignado_a']:
                print("Este miembro no está anotado en esta tarea.", "dark_grey")
            else:
                tareas[str(task_id)]['asignado_a'].remove(user_input)
                miembros[str(user_input)]['tareas_asignadas'].remove(task_id)
                tul.write_json(r"data/tasks.json", tareas)
                tul.write_json(r"data/member_data.json", miembros)

        print(colored("Operación exitosa.", "green"))
        sleep(1.3)


def assign_task_members(id_:str) -> None:
    """
    Permite al usuario administrar los miembros asignados a tareas.
    Recibe la ID del proyecto al que pertenece la tarea, en forma de string.
    No retorna nada.
    """
    proyectos = tul.read_json(r"data/project_data.json")
    tasks = tul.read_json(r"data/tasks.json")
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored("ASIGNAR MIEMBROS", "yellow"))
        if not proyectos[id_]['tareas']:
            print(colored("No hay tareas en este equipo.", "dark_grey"))
            print(colored("Presione ENTER para volver.", "dark_grey"))
            input()
            break

        for tarea in proyectos[id_]['tareas']:
            print(f"{tarea} - {tasks[str(tarea)]['nombre_tarea']}")
        print()

        try:
            task_input = int(input("Ingrese la ID de la tarea (-1 para cancelar): "))
            if task_input not in proyectos[id_]['tareas'] and task_input != -1:
                raise ValueError
        except ValueError:
            print(colored("ID no válida.", "red"))
            sleep(1.5)
            continue

        if task_input == -1:
            print(colored("Volviendo...", "red"))
            sleep(1.3)
            break

        manage_task_members(id_, task_input)


def manage_tasks(id_:str) -> None:

    """
    Permite al usuario modificar las tareas asignadas dentro de un equipo.
    Recibe la ID del proyecto en forma de string.
    No retorna nada.
    """

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored("ADMINISTRAR TAREAS", "yellow"))

        opciones = [
            "Ver tareas del proyecto",
            "Agregar tareas",
            "Editar estado de una tarea",
            "Asignar miembros a una tarea",
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
                see_tasks(id_)
            case 2:
                add_tasks(id_)
            case 3:
                edit_task_status(id_)
            case 4:
                assign_task_members(id_)
            case 5:
                print(colored("Volviendo...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)



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
                manage_tasks(id_)
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

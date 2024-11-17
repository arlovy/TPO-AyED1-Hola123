"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
from termcolor import colored
import regex as re
import modulos.tools as tul
import modulos.constantes as cons

def see_members() -> None:
    """
    Esta función permite visualizar a todos los miembros e información
    sobre ellos.
    No recibe ni retorna nada.
    """
    names = tul.read_csv(r"data/miembros.csv")
    groupnames = tul.read_csv(r"data/proyectos.csv")
    miembros = tul.read_json(r"data/member_data.json")
    roles = tul.read_json(r"data/roles.json")
    indent = "    "

    while True:
        tul.limpiar_pantalla()
        print(colored("VISTA GENERAL DE MIEMBROS", "yellow"))
        print()
        if not any(names):
            print(colored("No hay miembros cargados en el sistema. Presione ENTER para volver.",
                          "dark_grey"
                        )
                )
        else:
            for miembro, datos in names.items():
                #estas variables representan los datos de cada miembro,
                #primero agrupo todos los datos y luego los printeo
                id_ = f"{colored(f'(ID:{miembro})', 'yellow')}"
                nombre = datos['NOMBRE']
                dir_email = datos['EMAIL'] #saco la direccion aca por problemas con el fstring

                email = f"{colored(f'‣EMAIL: {dir_email}', 'dark_grey')}"
                print(f"{id_} - {nombre}")
                print(indent + email)

                if miembros[miembro]['roles']:
                    nombres_roles = [roles[str(rol)] for rol in miembros[miembro]['roles']]
                    roles_display = colored(" - ".join(nombres_roles), "dark_grey")
                else:
                    roles_display = colored("Este miembro no tiene roles asignados.", "dark_grey")
                print(indent + f"‣{roles_display}")

                print(indent + colored("GRUPOS DE TRABAJO:", "dark_grey"))
                grupos_miembro = miembros[miembro]['grupos_de_trabajo']
                if grupos_miembro:
                    for item in grupos_miembro:
                        print(
                            indent * 2 + colored(
                                f"‣{groupnames[str(item)]['NOMBRE DE PROYECTO']}","dark_grey"
                                )
                        )
                else:
                    print(
                        indent * 2 + colored(
                            "Este miembro no está anotado a ningun grupo.", "dark_grey"
                        )
                    )
                print() #un espacio vacío entre cada miembro

        salida = input(colored("Presione ENTER para salir: ", "yellow"))
        break


def crear_miembro() -> None:
    """
    Esta función permite crear un nuevo miembro y agrega registros tanto a
    miembros.csv como member_data.json.
    No recibe ni retorna nada.
    """
    patron_mail = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    names = tul.read_csv(r"data/miembros.csv")
    miembros = tul.read_json(r"data/member_data.json")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("CARGA DE MIEMBROS","yellow"))

        nombre = input("Ingrese el nombre del miembro (ENTER para salir): ")

        if not nombre:
            print(colored("Operación cancelada. Saliendo...", "red"))
            sleep(1)
            break
        else:
            while True:
                print("Ingrese la dirección de correo electrónico asociada a este miembro:")
                email = input()
                if re.match(patron_mail, email):
                    #lo cargo en el csv
                    idgen = int(list(names.keys())[-1]) + 1
                    names[str(idgen)] = {
                        'NOMBRE': nombre,
                        'EMAIL': email
                    }
                    tul.write_csv('data/miembros.csv', names)
                    #lo cargo en el json
                    miembros[str(idgen)] = {
                        "status": 1,
                        "roles": [],
                        "grupos_de_trabajo": [],
                        "tareas_asignadas": [],
                        "historial": []
                    }
                    tul.write_json('data/member_data.json', miembros)

                    print(colored("Miembro cargado correctamente.", "green"))
                    sleep(1.5)
                else:
                    print(colored(
                        "La dirección de correo electrónico no es válida. Intente nuevamente.","red"
                    )
                    )
                    sleep(1.5)
                break


def busqueda_por_id(id_:str, csvnombres: dict) -> None:
    """
    Esta función busca y muestra datos de un miembro basándose en una ID proporcionada.
    Recibe un ID en formato string y un diccionario que representa el CSV 'proyectos.csv'.
    No retorna nada.
    """
    miembros = tul.read_json(r"data/member_data.json")
    groupnames = tul.read_csv(r"data/proyectos.csv")
    roles = tul.read_json(r"data/roles.json")
    tasks = tul.read_json(r"data/tasks.json")
    indent = "    "

    nombre = csvnombres[id_]['NOMBRE']
    email = csvnombres[id_]['EMAIL']

    roles_id = miembros[id_]['roles']
    grupos_ids = miembros[id_]['grupos_de_trabajo']
    grupos_nombres = [ groupnames[str(grupo)]['NOMBRE DE PROYECTO'] for grupo in grupos_ids ]
    tareas = [tasks[str(task)] for task in miembros[id_]['tareas_asignadas']]

    print(colored("NOMBRE: ", "yellow") + nombre)
    print(colored("EMAIL: ", "yellow") + email)

    print(colored("ROLES:", "yellow"))
    if not roles_id:
        print(indent + "Este miembro no tiene roles asignados.")
    else:
        for rol in roles_id:
            print(indent + f"‣ {roles[str(rol)]}")

    print(colored("EQUIPOS:", "yellow"))
    if not grupos_ids:
        print(indent + "Este miembro no está anotado en ningun grupo de trabajo.")
    else:
        for id_, nombre in zip(grupos_ids, grupos_nombres):
            print(indent + f"{id_} - {nombre}")

    print(colored("TAREAS: ", "yellow"))
    if not tareas:
        print(indent + "Este miembro no tiene tareas asignadas.")
    else:
        for tarea in tareas:
            print(indent +
                colored(f"(PROYECTO {tarea['proyecto']})", "dark_grey") +
                    f" - {tarea['nombre_tarea']} " +
                colored(cons.task_status.get(tarea['status']), "dark_grey")
            )
    print("⸻⸻⸻" * 5) #un separador para que sea mas facil de leer


def buscar_miembro() -> None:
    """
    Inicializa la secuencia de búsqueda de miembros.
    No retorna ni recibe nada.
    """
    names = tul.read_csv(r"data/miembros.csv")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("BÚSQUEDA DE MIEMBROS: ", "yellow"))

        if not names: #revisa que hayan miembros cargados
            print(colored("No hay miembros cargados en el sistema. ENTER para volver."))
        else:
            tul.show_options(["Buscar por ID", "Buscar por nombre", "Volver"])

            try:
                user_input = int(input("Ingrese la opción: "))

            except ValueError:
                print(colored("Ingrese un número.", "red"))
                sleep(1.3)
                continue

            else:
                match user_input:
                    case 1:
                        id_ = input("Ingrese la ID: ")
                        if id_ not in names:
                            print(colored("ID no encontrada.", "dark_grey"))
                            print(colored("ENTER para volver.", "dark_grey"))
                        else:
                            tul.limpiar_pantalla()
                            busqueda_por_id(id_, names)
                    case 2:
                        name_query = input("Ingrese el nombre: ").lower()
                        coincidencias = list(
                            filter(lambda x: name_query in names[x]['NOMBRE'].lower(), names)
                        )

                        if not coincidencias or name_query in ["", " "]:
                            print(colored("Miembro no encontrado.", "dark_grey"))
                            print(colored("ENTER para volver.", "dark_grey"))
                        else:
                            tul.limpiar_pantalla()
                            for id_ in coincidencias:
                                busqueda_por_id(id_, names)

                    case 3:
                        print(colored("Volviendo...", "red"))
                        sleep(1.3)
                        break
        input()


def add_to_group(id_:str) -> None:
    """
    Añade un miembro a un grupo específico.
    Recibe una ID en forma de string.
    No retorna nada.
    """
    groupnames = tul.read_csv(r"data/proyectos.csv")
    grupos = tul.read_json(r"data/project_data.json")
    miembros = tul.read_json(r"data/member_data.json")

    print()
    #imprime los grupos disponibles para asignar al miembro.
    print(colored("GRUPOS DISPONIBLES:", "cyan"))
    for grupo, datos in groupnames.items():
        #muestro los grupos en los cuales no este anotado el miembro.
        if int(grupo) not in miembros[id_]['grupos_de_trabajo']:
            print(f"{grupo} - {datos['NOMBRE DE PROYECTO']}")
    print()

    grupo_target = input(
        "Ingrese la ID del grupo al cual desea agregar este miembro: "
    )
    #verifico si el grupo existe
    if grupo_target not in groupnames:
        print(colored("El grupo indicado no existe.", "dark_grey"))
    else:
        #verifico si el miembro no esta anotado ya
        if int(grupo_target) in miembros[id_]['grupos_de_trabajo']:
            print(colored("El miembro ya está en este grupo.", "dark_grey"))
        else:
            #los sumo a los diccionarios y escribo los archivos
            miembros[id_]['grupos_de_trabajo'].append(int(grupo_target))
            grupos[grupo_target]['miembros_asignados'].append(int(id_))
            tul.write_json('data/member_data.json', miembros)
            tul.write_json('data/project_data.json', grupos)

            print(colored("Operación exitosa.", "green"))
            print()


def modify_roles(id_:str) -> None:
    """
    Permite al usuario modificar los roels de un usuario específico.
    Recibe la ID del usuario en formato string.
    No retorna nada.
    """
    roles = tul.read_json(r"data/roles.json")
    miembros = tul.read_json(r"data/member_data.json")

    print()
    print(colored("ROLES:", "cyan"))
    for num, rol in roles.items():
        print(f"{num} - {rol}")
    print()

    tul.show_options(["Añadir rol a miembro", "Quitar rol a miembro", "Volver"])

    try:
        user_input = int(input("Ingrese la opción: "))
    except ValueError:
        print(colored("Elija una opción numérica.", "red"))
        sleep(1.5)
        print()
    else:
        match user_input:
            case 1:
                rol_input = input("Ingrese el rol: ")
                if rol_input not in roles:
                    print(colored("Este rol no existe.", "dark_grey"))
                else:
                    if int(rol_input) in miembros[id_]['roles']:
                        print(colored("Este miembro ya tiene este rol.", "dark_grey"))
                    else:
                        miembros[id_]['roles'].append(int(rol_input))
                        tul.write_json(r"data/member_data.json", miembros)
                        print(colored("Operación exitosa.", "green"))
                        sleep(1.3)
            case 2:
                if not miembros[id_]['roles']:
                    print(colored("El miembro no tiene roles asignados.", "dark_grey"))
                else:
                    print(colored("ROLES DEL MIEMBRO: ", "yellow"))
                    for rol in miembros[id_]['roles']:
                        if str(rol) in roles:
                            print(f"{rol}. {roles[str(rol)]}")

                    try:
                        rol_input = int(input("Ingrese el rol: "))
                    except ValueError:
                        print(colored("El rol ingresado no es válido.", "dark_grey"))
                    else:
                        if rol_input not in miembros[id_]['roles']:
                            print(colored("El miembro no tiene este rol.", "dark_grey"))
                        else:
                            miembros[id_]['roles'].remove(rol_input)
                            tul.write_json(r"data/member_data.json", miembros)
                            print(colored("Operación exitosa.", "green"))
                            sleep(1.3)


def edit_member_instance(id_:str) -> None:
    """
    Muestra opciones de edición para un miembro indicado en la función edit_member().
    Recibe un ID en formato string.
    No retorna nada.
    """

    print()
    while True:
        tul.show_options(["Añadir a un grupo", "Modificar roles", "Volver"])
        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)
            print()

        else:
            match user_input:
                case 1:
                    add_to_group(id_)
                case 2:
                    modify_roles(id_)
                case 3:
                    print(colored("Volviendo...", "red"))
                    sleep(1.3)
                    break
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.3)
                    print()


def edit_member() -> None:
    """
    Inicializa la secuencia de edición de miembros.
    No retorna ni recibe nada.
    """
    names = tul.read_csv(r"data/miembros.csv")

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("EDITAR MIEMBROS", "light_red"))

        if not names: #revisa que hayan miembros cargados
            print(colored("No hay miembros cargados en el sistema. ENTER para volver."))
        else:
            id_ = input("Ingrese la ID del miembro a editar (-1 para volver): ")
            if id_ == "-1":
                print(colored("Volviendo...", "red"))
                sleep(1.3)
                break

            if id_ not in names:
                print(colored("El miembro indicado no existe.", "dark_grey"))
                sleep(1.3)
            else:
                print()
                busqueda_por_id(id_, names)
                confirm = input("¿Desea editar este miembro? (S - SI / N - NO): ")
                if confirm.lower() == "s":
                    edit_member_instance(id_)
                else:
                    print(colored("Cancelando operación...", "red"))
                    sleep(1.3)


def gestion_miembros() -> None:
    """
    Esta función muestra las opciones del submenú de gestión de miembros y
    permite al usuario interactuar con el programa.
    """

    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("GESTIÓN DE MIEMBROS", "green"))
        opciones = [
            "Ver miembros",
            "Cargar un miembro",
            "Consultar por un miembro",
            "Editar un miembro",
            "Volver",
        ]
        tul.show_options(opciones)

        try:
            user_input = int(input("Ingrese la opción: "))
        except ValueError:
            print(colored("Elija una opción numérica.", "red"))
            sleep(1.5)

        else:
            match user_input:
                case 1:
                    see_members()
                case 2:
                    crear_miembro()
                case 3:
                    buscar_miembro()
                case 4:
                    edit_member()
                case 5:
                    print(colored("Volviendo al menú principal...", "red"))
                    sleep(1.5)
                    break
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)

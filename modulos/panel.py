"""
Este módulo maneja el código para la sección del panel de control general del programa.
"""

from time import sleep
from termcolor import colored
from tabulate import tabulate
import modulos.tools as tul
import modulos.constantes as cons

def progreso_proyecto(proyecto: dict, tasks: dict) -> float:
    """
    Devuelve un porcentaje de progreso para un proyecto en base
    al estado de sus tareas. 
    Recibe un diccionario que representa los datos de un proyecto, y
    el diccionario de tareas.
    Retorna un float que representa el porcentaje de progreso.
    """
    #saco la cantidad de tareas del proyecto
    total = len(proyecto["tareas"])
    #creo una lista con las id de las tareas del proyecto cuyo estado sea 3, osea
    #completado
    completas = [tarea for tarea in proyecto["tareas"] if tasks[str(tarea)]["status"] == 3]
    #si hay alguna tarea:
    if completas:
        #calcula el porcentaje
        return (len(completas) / total) * 100
    return 0


def reporte_general():
    """
    Esta función accede al JSON de proyectos, y genera un reporte del progreso,
    los miembros que trabajan y las tareas.
    No recibe nada, y no retorna nada.
    """
    #accedo a datos de todos los archivos para generar el reporte
    tareas = tul.read_json(r"data/tasks.json")
    proyectos = tul.read_json(r"data/project_data.json")
    miembros = tul.read_json(r"data/member_data.json")['miembros']
    names = tul.read_csv(r"data/miembros.csv")
    csv = tul.read_csv(r"data/proyectos.csv")

    archivos = [proyectos,csv]

    #verifico que todos los archivos se hayan ubicado exitosamente
    if all(archivos):
        tul.limpiar_pantalla()
        print(colored("REPORTE GENERAL - PRESIONE ENTER PARA SALIR", "green"))
        #el for genera un reporte por cada proyecto
        for proyecto in proyectos:
            #subreport es la pantalla a imprimir por cada proyecto usando tabulate
            subreport = []
            subreport.append(
                [colored(f"PROYECTO {proyecto}: {csv[proyecto]['NOMBRE DE PROYECTO']}", "cyan")]
            )
            progreso = 100 if proyectos[proyecto]['status'] == 3 else progreso_proyecto(proyectos[proyecto], tareas)
            #define una variable color dependiendo del progreso.
            if progreso <= 25:
                color = "red"
            elif progreso <= 50:
                color = "yellow"
            else:
                color = "green"

            #genera una barra de progreso para el proyecto
            subreport.append([f"PROGRESO: {progreso:.2f}%"])
            subreport.append([colored(tul.prog_bar(progreso), color)])

            #toma las ids de los integrantes dentro del proyecto
            integrantes = [
                item for item in miembros if int(proyecto) in miembros[item]['grupos_de_trabajo']
            ]

            if integrantes: #esto si hay miembros en el equipo
                subreport.append([colored("\nMIEMBROS DEL EQUIPO: ", "yellow")])

                #primero busco al integrante definido como lider en el json del proyecto
                if str(proyectos[proyecto]['leader']) in integrantes:
                    leadpos = integrantes.index(str(proyectos[proyecto]['leader']))
                    #hago un pop para imprimir al lider primero
                    lead = integrantes.pop(leadpos)
                    subreport.append(
                        [f"‣ {names[lead]['NOMBRE']} {colored('LIDER DE EQUIPO', 'green')}"]
                    )

                #luego printeo al resto
                for integrante in integrantes:
                    nombre_integrante = f"‣ {names[integrante]['NOMBRE']} "
                    #a partir de aca saco los roles de cada miembro, y los
                    #añado al final de sus nombres
                    roles_integrante = []
                    for item in miembros[integrante]['roles']:
                        roles_integrante.append(cons.roles.get(item))
                    sufijo = "-".join(roles_integrante)
                    subreport.append(
                        [nombre_integrante + colored(sufijo, "dark_grey")]
                    )
            else:
                subreport.append([colored("\nNo hay miembros anotados en el equipo.", "dark_grey")])

            #seccion de tareas
            if proyectos[proyecto]['tareas']:
                subreport.append([colored("\nTAREAS:", "yellow")])
                #defino el estado de cada tarea para armar un sufijo
                for tarea in proyectos[proyecto]['tareas']:
                    match tareas[str(tarea)]['status']:
                        case 1:
                            sufijo = colored('PENDIENTE','dark_grey')
                        case 2:
                            sufijo = colored('EN PROGRESO','yellow')
                        case 3:
                            sufijo = colored('COMPLETADA','green')

                    nombre_tarea = f"‣ {tareas[str(tarea)]['nombre_tarea']} " + sufijo
                    subreport.append([nombre_tarea])

                    #muestro al/los encargado/s de cada tarea
                    encargados  = []
                    for encargado in tareas[str(tarea)]['asignado_a']:
                        encargados.append(names[str(encargado)]['NOMBRE'])
                    encargados_str = ", ".join(encargados) + "\n"
                    subreport.append([colored(encargados_str, "dark_grey")])
            else:
                subreport.append([colored("\nNo hay tareas en este proyecto.", "dark_grey")])
            print(tabulate(subreport))
        salida = input()
    else:
        raise FileNotFoundError("Ha ocurrido un problema en la ubicación de archivos.")


def modificar_roles() -> None:
    """
    Esta función accede al JSON de roles y permite añadir roles personalizdaos.
    No recibe ni retorna nada.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        roles = tul.read_json("data/roles.json")
        print(colored("GESTIÓN DE ROLES DE TRABAJO\n", "magenta"))
        print(colored("ROLES ACTUALES:", "yellow"))
        for clave, valor in roles.items():
            print(f"{clave}. {valor}")
        print()
        print(colored("OPCIONES", "yellow"))
        opciones = [
            "Agregar un nuevo rol",
            "Volver"
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
                    nombre = input("Ingrese el nombre del rol: ")
                    print(f"Rol ingresado: {nombre}")
                    verify = input("¿Está seguro de que desea crear este rol? (S - SI / N - NO): ")
                    if verify.lower() == "s":
                        if roles:
                            ultima_clave = int(list(roles.keys())[-1])
                            roles[str(ultima_clave + 1)] = nombre
                        else:
                            roles[1] = nombre
                        op = tul.write_json("data/roles.json", roles)
                        if op:
                            print(colored("Operación exitosa.", "green"))
                            sleep(1.5)
                        else:
                            print(colored("Ha ocurrido un error en la escritura del archivo.", "red"))
                            sleep(1.5)
                    else:
                        print(colored("Cancelando operación...", "red"))
                        sleep(1.5)
                case 2:
                    print(colored("Volviendo...","red"))
                    sleep(1.5)
                    break
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)


def presentar_estadisticas():
    """
    Genera una serie de estadísticas y las presenta al usuario.
    No recibe ni retorna nada.
    """
    #accedo a datos de todos los archivos para generar estadisticas
    tareas = tul.read_json(r"data/tasks.json")
    proyectos = tul.read_json(r"data/project_data.json")
    miembros = tul.read_json(r"data/member_data.json")['miembros']
    names = tul.read_csv(r"data/miembros.csv")
    csv = tul.read_csv(r"data/proyectos.csv")

    archivos = [proyectos, csv]
    indent = "    " #una indentacion para organizar los datos
    if all(archivos):
        #seccion de tareas:
        print(colored("RENDIMIENTO DE TAREAS", "yellow"))
        #calculo el porcentaje de completado de las tareas
        rendimientos = tuple(tareas[tarea]['status'] for tarea in tareas)
        porcentajes = tuple(
            (i, rendimientos.count(i) / len(rendimientos) * 100) for i in set(rendimientos)
        )
        if porcentajes:
            print(indent + colored("COMPLETADO DE TAREAS:","cyan"))
            #muestra el porcentaje total de tareas
            print(indent * 2 + f"Total de tareas: {len(rendimientos)}")
            for item in porcentajes:
                print(indent * 2 + f"{cons.task_status.get(item[0])}: {item[1]:.2f}%")
            #muestra al miembro con más tareas completadas
            #primero calculo el maximo de tareas completadas
            maximo = max(len(miembros[x]['historial']) for x in miembros)
            #filtro, por si hubieran mas de 1 con la misma cantidad
            mve = list(filter(lambda x: len(miembros[x]['historial']) == maximo, miembros))
            #Printeo
            print(indent * 2 + colored("Miembro con más tareas completadas:", "green"))
            for memb in mve:
                print(
                    indent * 2 + f"‣ {names[memb]['NOMBRE']} " + colored(f"({maximo})", "dark_grey")
                )

            print(indent + colored("TAREAS POR PROYECTO:", "cyan"))
            

        else:
            print(indent* 2 + colored("No hay tareas creadas.", "dark_grey"))
        salida = input()    
    else:
        raise FileNotFoundError("Ha ocurrido un problema en la ubicación de archivos.")


def panel():
    """
    Inicializa la secuencia de panel de control para la aplicación principal.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("PANEL DE CONTROL DE SPM", "magenta"))
        opciones = [
            "Ver un reporte general de los proyectos",
            "Ver estadísticas de rendimiento",
            "Gestionar roles",
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
                    try:
                        reporte_general()
                    except FileNotFoundError as e:
                        print(colored(f"{e}", "red"))
                        sleep(1.5)
                case 2:
                    presentar_estadisticas()
                case 3:
                    modificar_roles()
                case 4:
                    print(colored("Volviendo al menú principal...", "red"))
                    sleep(1.5)
                    tul.limpiar_pantalla()
                    break  # rompe el while true y finaliza el programa
                case _:
                    print(colored("Opción no válida.", "red"))
                    sleep(1.5)
                    continue

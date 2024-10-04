"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
import re
import modulos.tools as tul
import modulos.constantes as cons
from termcolor import colored
from tabulate import tabulate


def cargar_miembro() -> None:
    """
    Esta función ejecuta la secuencia de carga de miembros en members.csv
    No recibe nada.
    No retorna nada.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("CARGA DE MIEMBROS", "green"))

        archivocsv = tul.abrir_csv("data/members.csv")

        # patron tal que Nombre Apellido
        patron_nombres = re.compile(
            "^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+$"
        )
        user_input = input(
            "Ingrese nombre y apellido del miembro a cargar (-1 para cancelar): "
        )
        nuevo_miembro = []  # inicializa el miembro a cargar en el csv

        if re.match(patron_nombres, user_input):  # si el nombre es valido
            nombre, apellido = user_input.split()  # divide el nombre en dos

            # añade la id y el nombre al nuevo miembro
            nuevo_miembro.extend([str(int(archivocsv[-1][0]) + 1), nombre, apellido])
            print()

            for key, valor in cons.SPECS.items():  # muestra los roles
                print(f"{key}. {valor}")
                print()

            user_input = input("Ingrese la especialidad: ")  # especialidad

            # aca se escribe en el csv
            if user_input in cons.SPECS:
                nuevo_miembro.extend([user_input])  # suma la especialidad al miembro

                with open(
                    "data/members.csv", "a", newline="", encoding="utf-8"
                ) as archivowrite:
                    archivowrite.write(f"{','.join(nuevo_miembro)}\n")

                print(colored("Usuario cargado correctamente.", "green"))
                sleep(1.5)
                break
            else:
                print("Especialidad no válida.")

        elif user_input == "-1":
            print(colored("Carga de miembro abortada...", "red"))
            sleep(1.5)
            break
        else:
            print("Error. El nombre debe seguir el formato 'Nombre Apellido'.")
        user_input = input("Presione ENTER para volver:")


def eliminar_miembro() -> None:
    """
    Esta función ejecuta la secuencia para dar de baja a miembros.
    No recibe nada.
    No retorna nada.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored("BAJA DE MIEMBROS", "red"))
        archivocsv = tul.abrir_csv("data/members.csv")

        id_input = input("Ingrese la ID del miembro a dar de baja (-1 para cancelar): ")

        if id_input == "-1" or id_input == "":
            print(colored("Cancelando operación", "red"))
            sleep(1.5)
            break
        else:
            if any(ide[0] == id_input for ide in archivocsv):  # se fija que la id exista
                for miembro in archivocsv:
                    if miembro[0] == id_input:  # busca el miembro con la id proporcioanda
                        dato = tuple(miembro)
                        break

                ide, nombre, apellido, spec = dato
                print(
                f"ID: {ide}\nNOMBRE: {nombre}\nAPELLIDO: {apellido}\nROL: {cons.SPECS.get(spec)}\n"
                )
                user_input = input(
                    "¿Desea dar de baja a este miembro? (1 - SI | 2 - NO): "
                )

                match user_input:
                    case "1":
                        for (
                            miembro
                        ) in archivocsv:  # busca el miembro con la id proporcioanda
                            if miembro[0] == id_input:  # si tiene id proprocioanda
                                miembro[3] = "-1"  # rol es -1

                        # abre el csv, lo reescribe desde 0
                        with open(
                            "data/members.csv", "w", newline="", encoding="utf-8"
                        ) as archivowrite:
                            for item in archivocsv:
                                # introduce cada fila de la matriz en el csv
                                archivowrite.write(f"{','.join(item)}\n")
                        print(colored("Miembro dado de baja correctamente...", "red"))
                        sleep(1.5)
                        break
                    case "2":
                        print(colored("Cancelando operación...", "red"))
                        sleep(1.5)
                        break
                    case _:
                        print(
                            colored("Opción no válida, cancelando operación...", "red")
                        )
                        sleep(1.5)
                        break
            else:
                print(colored("El usuario especificado no existe.", "red"))
                sleep(1.5)


def buscar_miembro() -> None:
    """
    Esta función debe permitir al usuario buscar miembros en el
    archivo CSV y mostrar su información.
    Debe permitir buscar por varias categorías.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("BUSCAR UN MIEMBRO", "green"))
        opciones = [
            "Ver todos los miembros",
            "Buscar por ID",
            "Buscar por especialidad",
            "Buscar por nombre",
            "Volver",
        ]
        tul.show_options(opciones)

        user_input = int(input("Ingrese la opción: "))
        archivocsv = tul.abrir_csv("data/members.csv")

        match user_input:
            case 1:  # VER TODOS
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                # hace el encabezado mas legible
                archivocsv[0] = [
                    "ID",
                    "Nombre",
                    "Apellido",
                    "Rol",
                ]
                # reemplaza valores enteros del rol por texto
                for fila in archivocsv:
                    fila[3] = cons.SPECS.get(fila[3])
                # printea la tabla, usa la primera fila como encabezado
                print(tabulate(archivocsv, headers="firstrow"))
                user_input = input("Presione ENTER para volver: ")

            case 2:  # BUSCAR POR ID
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                ides = tuple(item[0] for item in archivocsv) # trae las ids para comparar
                user_input = input("Ingrese la ID a buscar: ")

                if user_input in ides:  # si esta la id:
                    # filtra y trae al miembro
                    found = tuple(
                        list(filter(lambda x: x[0] == user_input, archivocsv)).pop(0)
                    )
                    # ^ el pop esta porque filter retorna [datos, ] asi que toma el primer valor
                    # y lo hace tupla
                else:
                    found = tuple()

                if found:
                    numid, name, lastn, role = (
                        found  # desempaqueta la tupla para printear
                    )
                    print(colored("USUARIO:", "green"))
                    print(
                    f"ID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}"
                    )
                else:
                    print("El usuario especificado no existe.")
                user_input = input("Presione ENTER para volver: ")

            case 3:  # BUSCAR POR ROL
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                for key, valor in cons.SPECS.items():  # muestra los roles
                    print(f"{key}. {valor}")
                print()
                user_input = input("Ingrese la opción: ")

                found = tuple(list(filter(lambda x: x[3] == user_input, archivocsv)))
                if found:
                    for fila in found:
                        numid, name, lastn, role = (
                            fila  # desempaqueta la tupla para printear
                        )
                        print(colored("USUARIO:", "green"))
                        print(
                        f"ID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}\n"
                        )
                else:
                    print(
                        colored(
                        "La especialidad indicada no es válida o no hay miembros con esa especialidad.",
                        "red",
                        )
                    )
                user_input = input("Presione ENTER para volver: ")

            case 4:  # BUSCAR POR NOMBRE
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                user_input = input("Ingrese el nombre a buscar: ").lower()
                found = tuple(
                    list(
                        filter(
                            lambda x: x[1].lower() in user_input.split()
                            or x[2].lower()
                            in user_input.split(),  # splitea por si nombre & apellido
                            archivocsv,
                        )
                    )
                )
                if found:
                    for fila in found:
                        numid, name, lastn, role = (
                            fila  # desempaqueta la tupla para printear
                        )
                        print(colored("USUARIO:", "green"))
                        print(
                        f"ID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}\n"
                        )
                else:
                    print("Ningún miembro coincide con el nombre ingresado.")
                user_input = input("Presione ENTER para volver: ")

            case 5:
                print(colored("Volviendo...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)


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
            "Cargar un miembro",
            "Eliminar un miembro",
            "Buscar un miembro",
            "Volver",
        ]
        tul.show_options(opciones)

        user_input = int(input("Ingrese la opción: "))

        match user_input:
            case 1:
                cargar_miembro()
            case 2:
                eliminar_miembro()
            case 3:
                buscar_miembro()
            case 4:
                print(colored("Volviendo al menú principal...", "red"))
                sleep(1.5)
                break
            case _:
                print(colored("Opción no válida.", "red"))
                sleep(1.5)

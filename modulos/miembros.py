"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
import csv
import modulos.tools as tul
import modulos.constantes as cons
from termcolor import colored
from tabulate import tabulate


def cargar_miembro():
    """
    Esta función debe acceder al archivo JSON de los miembros
    y permitir al usuario cargar uno nuevo.
    """


def eliminar_miembro():
    """
    Esta función debe permitir al usuario dar de baja miembros
    del archivo CSV. Deberá solicitar una confirmación antes
    de efectuar la eliminación. Al dar de baja, la especialidad
    en el CSV se establece en -1.
    """


def buscar_miembro():
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
        archivocsv = open("data/members.csv", newline="", encoding="utf-8")  # abre csv
        tabla_miembros = list(csv.reader(archivocsv))  # junta todos en una matriz
        archivocsv.close()

        match user_input:
            case 1:
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                # hace el encabezado mas legible
                tabla_miembros[0] = [
                    "ID",
                    "Nombre",
                    "Apellido",
                    "Rol",
                ]
                # castea todos los valores de rol a entero
                map(lambda x: int(x[3]), tabla_miembros)
                # reemplaza valores enteros del rol por texto
                for fila in tabla_miembros:
                    fila[3] = cons.SPECS.get(fila[3])
                # printea la tabla, usa la primera fila como encabezado
                print(tabulate(tabla_miembros, headers="firstrow"))
                user_input = input("Presione ENTER para volver: ")

            case 2:
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                user_input = input("Ingrese la ID a buscar: ")
                # itera y busca el usuario con la id tal
                # el filter retorna un objeto con lista, asi que hago un pop para hacerlo tupla
                found = tuple(
                    list(filter(lambda x: x[0] == user_input, tabla_miembros)).pop(0)
                )
                if found:
                    numid, name, lastn, role = (
                        found  # desempaqueta la tupla para printear
                    )
                    print(
                        f"USUARIO:\nID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}"
                    )
                else:
                    print("El usuario especificado no existe.")
                user_input = input("Presione ENTER para volver: ")

            case 3:
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                for key, valor in cons.SPECS.items():  # muestra los roles
                    print(f"{key}. {valor}")
                print()
                user_input = input("Ingrese la opción: ")

                found = tuple(
                    list(filter(lambda x: x[3] == user_input, tabla_miembros))
                )
                if found:
                    for fila in found:
                        numid, name, lastn, role = (
                            fila  # desempaqueta la tupla para printear
                        )
                        print(
                            f"USUARIO:\nID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}\n"
                        )
                else:
                    print(
                        "La especialidad indicada no es válida o no hay miembros con esa especialidad."
                    )
                user_input = input("Presione ENTER para volver: ")

            case 4:
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                user_input = input("Ingrese el nombre a buscar: ").lower()
                found = tuple(
                    list(
                        filter(
                            lambda x: x[1].lower() == user_input
                            or x[2].lower() == user_input,
                            tabla_miembros,
                        )
                    )
                )
                if found:
                    for fila in found:
                        numid, name, lastn, role = (
                            fila  # desempaqueta la tupla para printear
                        )
                        print(
                            f"USUARIO:\nID: {numid}\nNOMBRE: {name}\nAPELLIDO: {lastn}\nROL: {cons.SPECS.get(role)}\n"
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


def gestion_miembros():
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

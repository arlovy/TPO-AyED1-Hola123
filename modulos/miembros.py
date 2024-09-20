"""
Este módulo inicializa la secuencia de gestión de miembros.
"""

from time import sleep
import csv
import re
import modulos.tools as tul
import modulos.constantes as cons
from termcolor import colored
from tabulate import tabulate


def cargar_miembro():
    """
    Esta función debe acceder al archivo CSV de los miembros
    y permitir al usuario cargar uno nuevo.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("CARGA DE MIEMBROS", "green"))

        archivocsv = open("data/members.csv", newline="", encoding="utf-8")  # abre csv
        tabla_miembros = list(csv.reader(archivocsv))  # junta todos en una matriz
        archivocsv.close()

        patron_nombres = re.compile("^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+$") # patron tal que Nombre Apellido
        user_input = input("Ingrese nombre y apellido del miembro a cargar (-1 para cancelar): ")
        nuevo_miembro = [] #miembro a cargar en el csv

        if re.match(patron_nombres, user_input): #si el nombre es valido
            nombre, apellido = user_input.split() #divide el nombre en dos
            nuevo_miembro.extend([int(tabla_miembros[-1][0]) + 1, nombre, apellido]) # añade la id y el nombre al nuevo miembro
            print()

            for key, valor in cons.SPECS.items():  # muestra los roles
                print(f"{key}. {valor}")
                print()

            user_input = input("Ingrese la especialidad: ")  #especialidad

            #aca se escribe en el csv
            if user_input in cons.SPECS:
                nuevo_miembro.extend([user_input])
                with open('data/members.csv', "a", newline="", encoding="utf-8") as archivocsv:
                    escritor = csv.writer(archivocsv, delimiter=",", lineterminator="\n")
                    escritor.writerow(nuevo_miembro)
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
            case 1: #VER TODOS
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

            case 2: #BUSCAR POR ID
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                ides = [item[0] for item in tabla_miembros] #trae las ids para comparar
                user_input = input("Ingrese la ID a buscar: ")

                if user_input in ides: # si esta la id:
                    found = tuple(list(filter(lambda x: x[0] == user_input, tabla_miembros)).pop(0)) #filtra y trae al miembro
                    # el pop esta porque filter retorna [datos, ] asi que toma el primer valor y lo hce tupla
                else:
                    found = []

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

            case 3: #BUSCAR POR ID
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
                        colored("La especialidad indicada no es válida o no hay miembros con esa especialidad.",
                                "red"
                        )
                    )
                user_input = input("Presione ENTER para volver: ")

            case 4: #BUSCAR POR NOMBRE
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                user_input = input("Ingrese el nombre a buscar: ").lower()
                found = tuple(
                    list(
                        filter(
                            lambda x: x[1].lower() in user_input.split()
                            or x[2].lower() in user_input.split(), # splitea por si nombre & apellido
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

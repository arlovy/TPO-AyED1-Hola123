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
    Esta función debe acceder al archivo CSV de los miembros
    y permitir al usuario cargar uno nuevo.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()
        print(colored("CARGA DE MIEMBROS", "green"))

        archivocsv = tul.abrir_csv("data/members.csv")

        patron_nombres = re.compile("^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+$") # patron tal que Nombre Apellido
        user_input = input("Ingrese nombre y apellido del miembro a cargar (-1 para cancelar): ")
        nuevo_miembro = [] #miembro a cargar en el csv

        if re.match(patron_nombres, user_input): #si el nombre es valido
            nombre, apellido = user_input.split() #divide el nombre en dos
            nuevo_miembro.extend([str(int(archivocsv[-1][0]) + 1), nombre, apellido]) # añade la id y el nombre al nuevo miembro
            print()

            for key, valor in cons.SPECS.items():  # muestra los roles
                print(f"{key}. {valor}")
                print()

            user_input = input("Ingrese la especialidad: ")  #especialidad

            #aca se escribe en el csv
            if user_input in cons.SPECS:
                nuevo_miembro.extend([user_input])
                with open('data/members.csv', "a", newline="", encoding="utf-8") as archivowrite:
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
    Esta función debe permitir al usuario dar de baja miembros
    del archivo CSV. Deberá solicitar una confirmación antes
    de efectuar la eliminación. Al dar de baja, la especialidad
    en el CSV se establece en -1, no se borra la columna.
    """
    while True:
        tul.limpiar_pantalla()
        tul.printear_logo()

        print(colored("BAJA DE MIEMBROS", "red"))
        archivocsv = tul.abrir_csv("data/members.csv")
        id_input = input("Ingrese la ID del miembro a dar de baja (-1 para cancelar): ")

        if id_input != "-1" and id_input != "":
            for miembro in archivocsv:
                if miembro[0] == id_input: # busca el miembro con la id proporcioanda
                    dato = tuple(miembro)

            print(dato)
            ide,nombre,apellido,spec = dato
            print(f"ID: {ide}\nNOMBRE: {nombre}\nAPELLIDO: {apellido}\nROL: {cons.SPECS.get(spec)}\n")
            user_input = input("¿Desea dar de baja a este miembro? (1 - SI | 2 - NO): ")

            if user_input == "1":
                for miembro in archivocsv: # busca el miembro con la id proporcioanda
                    if miembro[0] == id_input: # si tiene id proprocioanda
                        miembro[3] = "-1" # rol es -1

                with open('data/members.csv', "w", newline="", encoding="utf-8") as archivowrite: # abre el csv, lo reescribe desde 0
                    for item in archivocsv: 
                        archivowrite.write(f"{item}\n") # introduce cada fila de la matriz en el csv

                print(colored("Miembro dado de baja correctamente...", "red"))
                sleep(1.5)
                break
            elif user_input == "2":
                print(colored("Cancelando operación...", "red"))
                sleep(1.5)
                break
            else:
                print(colored("Opción no válida. Cancelando operación...", "red"))
                sleep(1.5)
                break
        else:
            print(colored("Cancelando operación...", "red"))
            sleep(1.5)
            break


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
            case 1: #VER TODOS
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
                # castea todos los valores de rol a entero
                map(lambda x: int(x[3]), archivocsv)
                # reemplaza valores enteros del rol por texto
                for fila in archivocsv:
                    fila[3] = cons.SPECS.get(fila[3])
                # printea la tabla, usa la primera fila como encabezado
                print(tabulate(archivocsv, headers="firstrow"))
                user_input = input("Presione ENTER para volver: ")

            case 2: #BUSCAR POR ID
                # limpia pantalla
                tul.limpiar_pantalla()
                tul.printear_logo()

                ides = [item[0] for item in archivocsv] #trae las ids para comparar
                user_input = input("Ingrese la ID a buscar: ")

                if user_input in ides: # si esta la id:
                    found = tuple(list(filter(lambda x: x[0] == user_input, archivocsv)).pop(0)) #filtra y trae al miembro
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
                    list(filter(lambda x: x[3] == user_input, archivocsv))
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
                            archivocsv,
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

"""
Este módulo contiene funciones que son utilizadas por todo el programa.
"""

from os import system, name
import json
import datetime as dt
from tabulate import tabulate
from termcolor import colored
import modulos.constantes as cons

def printear_logo() -> None:
    """
    Esta función printea el logo de SPM usando tabulate. Trae
    el logo ASCII de SPM del archivo constantes.py
    """
    pantalla = [
        ["Software Project Manager by Hola123"],
        [colored(cons.LOGO, "blue")],
    ]  # elementos de la pantalla principal
    print(
        tabulate(pantalla, colalign=("center",))
    )  # printea pantalla principal con tabulate


def limpiar_pantalla() -> None:
    """
    Esta función se encarga de limpiar la consola.
    """
    # Para Windows
    if name == "nt":
        _ = system("cls")
    # Para Mac y Linux
    else:
        _ = system("clear")


def show_options(options: list[str]) -> None:
    """
    Esta función recibe una lista de strings y la imprime, enumerándola
    para permitir al usuario interactuar con el programa.
    """
    for numero, opcion in enumerate(options, start=1):
        print(f"{numero}. {opcion}")
    print()


def read_csv(ruta_csv: str) -> dict:
    """
    Esta función genera un diccionario a partir de un archivo CSV.
    Enumera los registros dentro del diccionario en base a su fila.

    Recibe como parámetro un string con la ruta del archivo CSV a leer.
    Retorna un diccionario. En caso de error retorna un diccionario vacío.
    """
    try:
        with open(ruta_csv, "rt", encoding="utf-8") as csvfile:
            #primero leo el csv, tomo el encabezado y luego
            #leo los registros y los guardo con una estructura
            #de matriz
            headers = csvfile.readline().strip().split(",")
            data = list(map(lambda x: x.strip().split(","), csvfile.readlines()))

            #defino un diccionario donde cargar cada registro del csv,
            #uso diccionarios mas que nada porque facilita el acceso a
            #los datos más tarde
            registros = {}

            #asumiendo que la primera columna sea la ID
            #revisa que haya un campo mas ademas de la id
            if len(headers) > 1:
                for linea in data:
                    #lee a partir del campo 1, es decir el siguiente a la id
                    registros[linea[0]] = {headers[i]: linea[i] for i in range(1,len(headers))}
    except FileNotFoundError:
        registros = {}
    return registros


def write_csv(ruta_csv: str, diccionario: dict) -> bool:
    """
    Escribe los datos de un diccionario generado con read_csv() a un archivo especificado.
    **IMPORTANTE**: Esta función sobreescribe el CSV indicado, si existiera.
    Recibe un string con la ruta del CSV, y un diccionario con los datos.
    Retorna un valor booleano que indica si la operación se realizó con éxito.
    """
    #hice esta función por cuestiones de legibilidad en los modulos, prefiero dejarla aca y reducir
    #las lineas en el resto de archivos a la hora de escribir en un csv.
    if diccionario:
        try:
            with open(ruta_csv, "wt", encoding="utf-8") as csvfile:
                #establece los headers basandose en las claves del primer elemento
                primero = list(diccionario.keys())[0]
                csvfile.write("ID," + ",".join(diccionario[primero].keys()) + "\n")
                #escribe los valores de cada registro
                for key in diccionario:
                    registro = f"{key}," + ",".join(map(str,diccionario[key].values())) + "\n"
                    csvfile.write(registro)
        except FileNotFoundError:
            return False
        return True #booleanos para printear mensajes después


def read_json(ruta_archivo: str) -> dict:
    """
    Lee un archivo JSON en la ruta especificada y lo retorna como un diccionario.
    Recibe un string con la ruta del archivo.
    Retorna el archivo JSON como un diccionario.
    """
    try:
        with open(ruta_archivo, 'rt', encoding='utf-8') as archivo:
            diccionario = json.load(archivo)
    except FileNotFoundError:
        return {}
    return diccionario


def write_json(ruta_archivo:str, diccionario:dict) -> bool:
    """
    Escribe un diccionario como un archivo JSON en la ruta especificada. 
    Recibe un string con la ruta del archivo y un diccionario.
    Retorna un valor booleano que indica si la operación se realizó con éxito.
    """
    try:
        with open(ruta_archivo, 'wt', encoding='utf-8') as archivo:
            myjson = json.dumps(diccionario)
            archivo.write(myjson)
    except FileNotFoundError:
        return False
    return True


def prog_bar(percent: int) -> str:
    """
    Genera una barra de progreso de 10 segmentos en base a un
    porcentaje especificado.
    Recibe un entero.
    """
    #defino caracteres a usar para progreso lleno o vacio
    full = "█" #valor completo
    null = "░" #valor vacio

    #define la cantidad de segmentos a rellenar en una barra de 10
    #si quisiera hacer una barra más larga, cambiar el 10 por la longitud
    #deseada
    progress = (percent * 10) // 100

    #genera la barra final
    barra = full * int(progress) + null * (10 - int(progress))
    return barra

def to_datetime(date:str) -> object:
    """
    Convierte una fecha formato "AAAA-MM-DD" en un objeto datetime.
    """
    #teniendo en cuenta que el formato usado por los json es AAAA-MM-DD
    year,month,day = list(map(int,date.split("-")))
    date = dt.datetime(year,month,day)
    return date

def get_date() -> str:
    """
    Trae la hora actual en formato AAAA-MM-DD.
    Retorna un string y no recibe parámetros.
    """
    return str(dt.date.today())

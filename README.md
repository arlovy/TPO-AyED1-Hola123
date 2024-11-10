<p align="center">
    <img src="https://i.imgur.com/5gBk8EU.gif" alt="Logo">
    <img src="https://i.imgur.com/B2YVNwO.gif" alt="Texto">
</p>

# Integrantes

- Lucas Paluci
- Aron Lovey
- Gabo Esperon
- Maximo Escobar Gallo

# Sobre el programa
Esta es un programa de seguimiento de proyectos de desarrollo de software, que básicamente permite gestionar grupos de trabajo en el contexto de una empresa de software. La aplicación permite crear proyectos, asignar tareas dentro de ellos, y permite a los gerentes consultar el progreso de cada equipo.

El programa trabaja con 2 CSV; **members.csv**, que contiene a los miembros, y **groups.csv**, que contiene los distintos proyectos y sus IDs. Luego está el archivo **projects.json** que contiene la información de cada grupo de trabajo.

Las principales librerías usadas son:
- **TABULATE:** Para la organización de la interfaz y la presentación de datos.
- **JSON:** Para trabajar con archivos JSON.
- **TERMCOLOR:** Utilizado para darle color a textos en la terminal, mas que nada para facilitar la lectura.
- **TIME:** Mas que nada la función sleep, para dejar un tiempo entre los mensajes de error y salida antes de limpiar la terminal.
- **OS:** Utilizado para limpiar la terminal al cambiar entre pantallas.

El texto ASCII que se utiliza como logo a lo largo del programa fue generado en esta pagina:
- https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

## Organización del programa
El programa se basa en el archivo **aplicacion.py**, que llama a los módulos **miembros.py** y **proyectos.py** para ejecutar sus funciones. Adicionalmente, el módulo **tools.py** contiene funciones utilizadas por el resto de módulos, como la función **limpiar_pantalla()** o **show_options()** que es usada por todos los menús. 

En el directorio **data** se encuentran los archivos de datos CSV y JSON.

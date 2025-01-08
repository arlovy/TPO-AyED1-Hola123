<p align="center">
    <img src="https://i.imgur.com/5gBk8EU.gif" alt="Logo">
    <img src="https://i.imgur.com/B2YVNwO.gif" alt="Texto">
</p>

# Sobre el programa
Esta es un programa de seguimiento de proyectos de desarrollo de software, que básicamente permite gestionar grupos de trabajo en el contexto de una empresa de software. La aplicación permite crear proyectos y dentro de ellos asignar tareas a miembros, generando reportes y estadísticas en base al progreso de cada equipo. 

El programa trabaja con los miembros a través de los archivos **miembros.csv**, donde se guardan los nombres y las direcciones de correo, y **member_data.json**, que incluye toda la información dinámica de cada miembro (su equipo de trabajo, las tareas en las que se desempeña, sus roles, etc). También hace uso de los archivos **proyectos.csv** y **project_data.json** para gestionar la información relacionada a los grupos de trabajo. Finalmente, con **tasks.json** se maneja la información de cada tarea.

Las principales librerías usadas son:
- **TABULATE:** Para la organización de la interfaz y la presentación de datos.
- **JSON:** Para trabajar con archivos JSON.
- **TERMCOLOR:** Utilizado para darle color a textos en la terminal, mas que nada para facilitar la lectura.
- **TIME:** Mas que nada la función sleep, para dejar un tiempo entre los mensajes de error y salida antes de limpiar la terminal.
- **OS:** Utilizado para limpiar la terminal al cambiar entre pantallas.

El texto ASCII que se utiliza como logo a lo largo del programa fue generado en esta pagina:
- https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

## Organización del programa
El programa se basa en el archivo **aplicacion.py**, que llama a los módulos **miembros.py**, **proyectos.py** y **panel.py** para ejecutar sus funciones. Adicionalmente, el módulo **tools.py** contiene funciones utilizadas por el resto de módulos, como la función **limpiar_pantalla()** o **show_options()** que es usada por todos los menúes. 

En el directorio **data** se encuentran los archivos de datos CSV y JSON.

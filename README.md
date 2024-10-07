# Workflow-managers
Seguir el tutorial, modificarlo y generar un ejemplo.

# Prefect
Se trata de una herramienta del tipo orquestador de flujo de trabajo especializado en el monitoreo.

# Heramientas utilizadas
En este ejemplo se utiliza la versión 1.4 de prefect ya que apartir de la version 2.0 en adelante cambia el funcionamiento de la biblioteca.

- Prefect < 2.0
- SQLite
- JSON Placeholder (API)

# Ejemplo modificado
Es necesario agregar el decorador `@task` en cada funcíon que utilicemos en el flujo de trabajo

### Crear flujo
```
with Flow("my etl flow", schedule) as f:
    db_table = create_table()
    raw = get_todo_data()
    parsed = parse_todo_data(raw)
    populated_table = store_todos(parsed)
    populated_table.set_upstream(db_table)
    todos = first_five_user_todos()
    show_todos(todos)
    todos = uncompleted_user_todos()
    show_todos(todos)
f.run()
```

### Crear intervalo de repetición del flujo
> #### `schedule = IntervalSchedule(interval=timedelta(minutes=1))`
>
> Repite el flujo al pasar el tiempo determinado. Se asimila a la función `sleep()`

### Funciones
> `create_table()`
>
> Se encarga de crear la tabla SQLite en caso de ser necesario

> `get_todo_data()`
>
> Fetch a la API JSON placeholder para obtener los TODO

> `parse_todo_data()`
>
> Pasar los valores obtenidos en el fetch a una lista

> `store_todos()`
>
> Guardar la lista en la base de datos

> `first_five_user_todos()`
>
> Obtener las primeras 5 tareas del usuario


> `uncompleted_user_todos()`
>
> Obtener las primeras 5 tareas no completadas del usuario

> `show_todos()`
>
> Mostrar las tareas en forma de tabla

# Resultados
> Ejecución del programa correctamente
<img src="https://github.com/jhotwox/Workflow-managers/blob/main/correcto1.png?raw=true">

> Repetición debido a que paso el minuto asignado en el intervalo
<img src="https://github.com/jhotwox/Workflow-managers/blob/main/correcto2.png?raw=true">

> Error debido a que modifique la linea 30 en la función `parse_todo_data()` para que no se guarde si la tarea fue completada o no
<img src="https://github.com/jhotwox/Workflow-managers/blob/main/error.png?raw=true">
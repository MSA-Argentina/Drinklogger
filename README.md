Drinklogger
===========

Introducción
------------

En la oficina se necesitaba una forma eficiente de manejar la compra y stock de bebidas, y por ello surgió Drinklogger. El objetivo es que uno en pocos pasos pueda dejar marcado qué bebida tomó, en qué momento y el precio en el que estaba en ese momento (debido a que el precio de la bebida puede cambiar con el tiempo). También, tiene una ABM (Flask) para que cualquiera sea el encargado pueda agregar usuarios y el stock a la base de datos (PostgreSQL).

Requerimientos
--------------

* Python 2 (Python 3 no probado)
* PostgreSQL

Instalación
------------

Clonar el repositorio

    git clone https://github.com/MSA-Argentina/Drinklogger.git

Crear un entorno virtual con **virtualenvwrapper**

    mkvirtualenv drinklogger

O tan sólo **virtualenv**.

    virtualenv drinklogger

Luego, ejecutar el archivo _requeriments.txt_ con **pip**.

    pip install -r requirements.txt

Después, si no hubo errores en la instalación de los requerimientos, editar el archivo _config.py_ en las siguientes líneas:

    # Configuracion
    DATABASE = {
        'name': '',
        'engine': '',
        'user': '',
        'pass': '',
    }

    DEBUG = False # Activar fuera del repo
    SECRET_KEY = '' # Agregar fuera del repo

Agregando el nombre de la base de datos, el motor (Por default usamos **PostgreSQL**), el usuario, la contraseña de la base de datos y agregar un valor a *SECRET_KEY*. Si se está probando, es recomendable cambiar _DEBUG_ de **False** a **True**.

Y finalmente, ejecutar el archivo *main.py*.

    python main.py

F.A.Q.
------

Estos son posibles errores que puede haber en la instalación.

### No se puede instalar psycopg2

En **Linux**, instalar _python-dev_ y _postgresql-server-dev-9.3_ para que psycopg2 pueda compilar.

    sudo apt-get install python-dev postgresql-server-dev-9.3

En **Windows** usar [el instalador gráfico](http://stickpeople.com/projects/python/win-psycopg/).

### ¿Se puede usar SQLite o MySQL?

Sí, ambos son soportados. Pero en vez de **psycopg2** tiene que instalar **pysqlite** para _SQLite_ y **mysql-connector-repackaged** en _MySQL_.

### ¿Cómo creo un usuario para la administración?

Para crear un usuario **admin** default necesitan correr este código python desde la línea de comando o mismo desde el _____main_____

    from config import auth
    auth.User.create_table(fail_silently=True)  # make sure table created.
    admin = auth.User(username='admin', email='', admin=True, active=True)
    admin.set_password('admin')
    admin.save()

Una vez corrido, pueden entrar como usuario **admin** y password **admin**. Es recomendable cambiar esto.

### ¿Cómo puedo contribuír?

* Forkeá
* Crea un branch nuevo
* Hace los cambios
* Tirá un pull request :)

Licencia
--------

[Ver licencia](https://raw.githubusercontent.com/MSA-Argentina/Drinklogger/master/LICENSE).
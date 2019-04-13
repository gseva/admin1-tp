
## Trabajo Práctico grupal de Proyectos Informáticos (75.18/75.44)

Es una aplicación web simple hecha con [Flask-AppBuilder](https://flask-appbuilder.readthedocs.io/en/latest/).
Se probó con Python 3.7, pero deberia funcionar con Python >= 3.5

### Setup

Para instalar y correr la aplicación hay que hacer lo siguiente:

0. (Opcional, pero recomendable) Crear un entorno virtual para no
instalar las dependencias globales.

 - Instalar [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

 - Crear entorno virtual:

```bash
cd /alguna/ruta/para/virtualenvs
virtualenv admin1 --python python3
```

 - Activar entorno virtual:

```bash
source admin1/bin/activate
```

Una vez activado el entorno, todas las dependencias de Python se van a instalar
solo para ese entorno.

1. Instalar las dependencias del proyecto:

```bash
cd /ruta/a/admin1-tp
pip install -r requirements.txt
```

2. Crear usuario Administrador

```bash
# Este comando interactivamente preguntará datos del administrador
fabmanager create-admin
```

3. Correr la aplicación

```bash
fabmanager run
```

Listo, la aplicación se debería poder acceder en `localhost:8080`.

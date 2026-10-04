# Tarea AE2 — Calculadora Web con nginx + Gunicorn

## Stack elegido

Se ha elegido el stack Python:

-   Flask como framework de la aplicación.
-   Gunicorn como servidor de aplicaciones WSGI.
-   nginx como servidor web y proxy inverso.
-   Docker Compose para el entorno dockerizado.

## 1. Instalación

### Entorno nativo

La práctica se realiza dentro del contenedor de laboratorio `dpl-lab`, basado en Ubuntu.

Antes de instalar los servicios, se configuró `policy-rc.d` para evitar que los paquetes intentasen arrancar servicios automáticamente mediante `systemd` ya que el contenedor no lo utiliza.

```bash
docker exec dpl-lab bash -c 'printf "#!/bin/sh\\nexit 101\\n" > /usr/sbin/policy-rc.d && chmod +x /usr/sbin/policy-rc.d'  
```
Se actualizaron los repositorios e instalaron Python, el módulo para entornos virtuales, nginx y curl:

```bash
docker exec dpl-lab apt-get update  
docker exec dpl-lab apt-get install -y python3 python3-venv nginx curl  
```
Versiones comprobadas:

```bash
Python 3.12.3  
nginx version: nginx/1.24.0 (Ubuntu)  
curl 8.5.0  
```

El proyecto se encuentra en:

```bash
/home/aperez/dpl/ae2  
```

### Entorno virtual y dependencias

La aplicación utiliza un entorno virtual de Python para mantener aisladas sus dependencias. Esto también evita el problema `externally-managed-environment` asociado a las instalaciones de paquetes Python en el sistema.

El fichero `nativo/web/requirements.txt` contiene:

```bash
flask==3.1.0  
gunicorn==23.0.0  
```

El entorno virtual se creó en la raíz del microproyecto:

```bash
docker exec dpl-lab bash -c 'cd /home/aperez/dpl/ae2 && python3 -m venv .venv'  
```

Las dependencias se instalaron utilizando el `pip` del entorno virtual:

```bash
docker exec dpl-lab bash -c 'cd /home/aperez/dpl/ae2 && .venv/bin/pip install -r nativo/web/requirements.txt'  
```

La instalación se comprobó con:

```bash
docker exec dpl-lab bash -c 'cd /home/aperez/dpl/ae2 && .venv/bin/pip list | grep -iE "flask|gunicorn"'  

Flask        3.1.0
gunicorn     23.0.0
```

El entorno virtual `.venv/` no se versiona mediante Git porque contiene dependencias instaladas y puede regenerarse a partir de `requirements.txt`.

## 2. Crear la calculadora Flask

La aplicación web se implementa con Flask y realiza los cálculos en el servidor mediante Python. No se utiliza JavaScript para realizar las operaciones.

La aplicación principal se encuentra en:

```bash
nativo/web/app.py
```

El fichero contiene las operaciones de suma, resta, multiplicación y división, además de la validación de los operandos y la comprobación de división entre cero.

La aplicación dispone de una ruta GET para mostrar el formulario y una ruta POST para procesar los datos enviados por el usuario.

La plantilla HTML se encuentra en:

```bash
nativo/web/templates/index.html
```
La plantilla contiene el formulario de la calculadora y muestra el resultado del cálculo o el mensaje de error correspondiente.

El título utilizado para identificar el entorno nativo es `Calculadora en entorno nativo`

Los estilos de la aplicación se encuentran en:

```bash
nativo/web/estilos.css
```

Los archivos creados se comprobaron con:

```bash
ls -l nativo/web/app.py
ls -l nativo/web/estilos.css
ls -l nativo/web/templates/index.html
```

Los tres archivos existen correctamente y quedan preparados para ejecutar la aplicación mediante Gunicorn y publicarla posteriormente a través de nginx.

# SistemasExpertoII2025

## para replicar el entorno de desarrollo

`CALL grupo4-app/Scripts/activate`

## para colectar las dependencias del proyecto

`python -m pip install -r requirements.txt`

## cuando añadan dependencias extra (sí lo hacen)

`python -m pip freeze > requirements.txt` y editan el archivo de requerimientos

## para generar un archivo ejecutable del proyecto

`nuitka [--standalone || --onefile --onefile-windows-splash-screen-image="splash.png"] --disable-console --enable-plugin=<requirements>`
donde `<requirements>` es la lista de dependencias en el archivo de `requirements.txt` (debe haber un comando por cada dependencia) y la opción "standalone" o "onefile" es para el tipo de ejecutable, si será un solo archivo (`--onefile`) o el archivo con sus dependencias (`--standalone`), decidan xd; y finalmente `--disable-console` es para desactivar la consola durante la ejecución del programa

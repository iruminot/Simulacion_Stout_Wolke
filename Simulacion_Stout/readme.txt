SIMULACION BOBINA-LANZA STOUT

Por: Ignacio Ruminot Aburto - ignacio.ruminot@wolke.cl
Cargo: Ingeniero de Modelamiento y Control de Procesos Hídricos 

SOFTWARE NECESARIO: 
	
	A three-dimensional finite element mesh generator: GMSH https://gmsh.info/bin/Windows/gmsh-4.13.1-Windows64.zip
	General Environment for the Treatment of Discrete Problems: GETDP https://getdp.info/bin/Windows/getdp-3.5.0-Windows64c.zip

La carpeta "Simulación_Stout" contiene los archivos necesarios para ejecutar la simulación de una bobina
a la cual se le suministra una corriente electrica para inducir un campo electromagnetico que induce
un cambio de temperatura en una lanza que se introduce en la bobina.

Los archivos que contiene esta carpeta son los siguientes:

1) extract.py: para extraer datos de temperatura de los archivos "temp.pos" y transformarlos a ".csv"
2) magneto_thermal.pro: archivo que contiene codigo de ejecución de simulación
3) magneto_thermal.msh: archivo que contiene el mallado a utilizar
4) magneto_thermal.geo: archivo que contiene la definicion de geometría
5) run_getdp.sh: archivo utilizado para automatizar la ejecución de simulaciones
6) run.sbatch: archivo utilizado para ejectuar simulación en clúster
7) readme.txt: archivo con indicaciones e información

Las simulaciones se pueden ejecutar directamente desde la aplicación GMSH, pero al ser una herramienta
gráfica se necesitará mucho computo y memoria, lo que implica más tiempo de ejecución. Para disminuir
dicho tiempo se recomienda realizar las ejecuciones por consola.

	## TENER EN CUENTA QUE TODOS LOS COEFICIENTES ESTAN EN SISTEMA INTERNACIONAL DE UNIDADES ##

¿COMO EJECUTAR UNA SIMULACIÓN?

	## RECORDAR QUE PARA EJECUTAR POR CONSOLA SE DEBE AGREGAR GMSH Y GETDP AL PATH ##

Para ejecutar una simulación desde la aplicación GMSH, se debe tener el archivo ".msh" (si no se tiene, el
archivo ".geo" generara el ".msh" y luego ejecutará la simulación). Se debe ejecutar el archivo ".pro" este
procede de la siguiente manera:

i) Chequea si existe el archivo ".msh", si no existe, ejecutará primero el archivo ".geo" generando el
   mallado ".msh".
ii) Una vez verifica que se tiene el archivo ".msh", procede a ejecutar el ".pro" preprocesando, procesan-
    do, postprocesando y postoperando.
iii) Como resultado se obtienen archivos ".txt", ".pos".
iv) Utilizar el archivo ".py" para extraer los datos necesarios

¿UNA MANERA MÁS EFICIENTE? 
Para ejecutar la simulación de una manera mas eficiente, se recomienda ejecutar todo por consola:

i) Para generar un mallado con tamaño de triángulo máximo, se debe cambiar en el archivo ".msh" el tamaño
   deseado (por defecto tiene 0.001), luego se debe ejecutar la siguiente linea de comando en consola

	>> gmsh -3 <nombre>.geo -nt <entero> -part <entero> -format msh2 -o <nombre_guardado>.msh

	-3: indica que es 3D
	-nt: numero de threads a utilizar (depende del procesador), se puede eliminar
  	-part: numero de particiones para distribuir por procesador, se puede eliminar
	-format msh2: formato para almacenar el mallado
	-o: para indicar que se va a indicar un nombre de guardado

   Por ejemplo:
		
	>> gmsh -3 magneto_thermal.geo -nt 8 -part 8 -format msh2 -o magneto_thermal.msh

ii) Para la simulación se debe ejecutar la siguiente linea de comando en consola:
	
	>> getdp <nombre>.pro -solve -v2 -pos -msh <nombre_mallado>.msh

	-solve: indica que debe resolver
	-v2: que muestre proceso de ejecución por consola
	-pos: ejecute el postprocesamiento
	-msh: indica que vas a utilizar un mallado

   Por ejemplo

	>> getdp magneto_thermal.pro -solve -v2 -pos -msh magneto_thermal.msh

   La ejecución te pedirá ingresar el tipo de formulación y la resolución a utilizar, se debe ingresar
   3 - 1 para la parte electromagnetica, que se ejecute y procese y luego volver a ejecutar, pero con
   las entradas 3 - 3 para la parte de difusión de calor.

   Por ejemplo:

	>> getdp magneto_thermal.pro -solve -v2 -pos -msh magneto_thermal.msh
	>> 3
	>> 1

	>> getdp magneto_thermal.pro -solve -v2 -pos -msh magneto_thermal.msh
	>> 3
	>> 3

¿COMO AUTOMATIZAR EL PROCESO?
Para automatizar la ejecución, se utilizar el archivo ".sh", este archivo se usa para ejecutar comandos
automaticos por consola. El archivo esta fijado en 3 iteraciones de simulación, con 30kHz,70kHz y 100kHz".
Para ejecutar por linea de comando:

	>> chmod +x run_getdp.sh
	>> ./run_getdp.sh

Se deben tener 3 archivos para que se ejecute el ".sh":
1) 30kHz: magneto_thermal_1.pro
2) 70kHz: magneto_thermal_2.pro
3) 100kHz: magneto_thermal_3.pro 

Los resultados de cadad simulación son almacenados en una carpeta de nombre "Simulacion_*.

¿COMO VISUALIZAR LOS DATOS?
para poder ver animaciones de los datos generados, se deben correr los archivos ".pos" en GMSH para poder visualizar animaciones en paso de tiempo.

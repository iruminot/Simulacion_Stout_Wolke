#!/bin/bash

# Nombre base del archivo
BASE_NAME="magneto_thermal"

# Nombre del archivo de log general
LOG_FILE="getdp_batch_output.log"

# Borrar log anterior si existe
> "$LOG_FILE"

# Iterar sobre los archivos numerados del 1 al 6
for i in {1..3}; do
    PRO_FILE="${BASE_NAME}_${i}.pro"

    # Verificar si el archivo existe antes de ejecutarlo
    if [ -f "$PRO_FILE" ]; then
        echo "Ejecutando GetDP con $PRO_FILE..." | tee -a "$LOG_FILE"
        
        # Crear carpeta para almacenar resultados de la iteración
        OUTPUT_DIR="Simulacion_$i"
        mkdir -p "$OUTPUT_DIR"

        # Primera ejecución con entrada (1,2)
        echo "Ejecutando con entrada (3,1)..." | tee -a "$LOG_FILE"
        printf "3\n1\n" | getdp "$PRO_FILE" -solve -v2 -pos -msh magneto_thermal.msh | tee -a "$LOG_FILE"

        # Segunda ejecución con entrada (1,1)
        echo "Ejecutando con entrada (3,3)..." | tee -a "$LOG_FILE"
        printf "3\n3\n" | getdp "$PRO_FILE" -solve -v2 -pos -msh magneto_thermal.msh | tee -a "$LOG_FILE"

        # Mover los archivos generados a la carpeta correspondiente
        echo "Moviendo archivos generados a $OUTPUT_DIR..." | tee -a "$LOG_FILE"
        mv *.pos *.res *.pre *.log *.txt "$OUTPUT_DIR" 2>/dev/null

        echo "Ejecuciones completadas para $PRO_FILE. Datos almacenados en $OUTPUT_DIR." | tee -a "$LOG_FILE"

    else
        echo "Archivo $PRO_FILE no encontrado. Omitiendo..." | tee -a "$LOG_FILE"
    fi

    echo "======================================" | tee -a "$LOG_FILE"
done

echo "Proceso finalizado. Revisa $LOG_FILE para ver los resultados."

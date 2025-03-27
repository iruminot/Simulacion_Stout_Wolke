import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def leer_archivo_pos(ruta_archivo):
    # Lista para almacenar todos los DataFrames de cada iteración
    dataframes = []

    # Variables temporales
    datos_iteracion = []
    iteracion_actual = 0  # Contador de iteraciones

    # Abrir el archivo y leer línea por línea
    with open(ruta_archivo, 'r') as file:
        lineas = file.readlines()

        # Índice para rastrear la posición en las líneas
        indice = 0

        # Recorrer cada línea del archivo
        while indice < len(lineas):
            linea = lineas[indice].strip()

            # Si encontramos la línea que indica el inicio de los datos
            if linea.startswith("$ElementNodeData"):
                # Saltar líneas hasta encontrar la secuencia de números
                indice += 1
                while indice < len(lineas):
                    linea = lineas[indice].strip()

                    # Si encontramos la línea que indica el fin de los datos
                    if linea.startswith("$EndElementNodeData"):
                        break

                    # Si la línea contiene una secuencia de números, extraer los datos
                    if any(c.isdigit() or c == "." for c in linea):  # Verificar si hay números o puntos
                        valores = linea.split()
                        if len(valores) >= 3:  # Asegurarse de que la línea tenga suficientes valores
                            datos_iteracion.append(valores)

                    # Avanzar a la siguiente línea
                    indice += 1

                # Si hay datos en la iteración actual, crear un DataFrame
                if datos_iteracion:
                    # Determinar el número máximo de columnas
                    max_columnas = max(len(fila) for fila in datos_iteracion)

                    # Crear nombres de columnas
                    nombres_columnas = ["Iteracion", "Elemento", "Nodos"] + [f"Valor_{i+1}" for i in range(max_columnas - 2)]

                    # Agregar la iteración a los datos
                    datos_con_iteracion = [[iteracion_actual] + fila for fila in datos_iteracion]

                    # Crear el DataFrame
                    df = pd.DataFrame(datos_con_iteracion, columns=nombres_columnas)
                    dataframes.append(df)

                    # Incrementar el contador de iteraciones
                    iteracion_actual += 1

                # Reiniciar las variables para la siguiente iteración
                datos_iteracion = []

            # Avanzar a la siguiente línea
            indice += 1

    # Combinar todos los DataFrames en uno solo
    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        return df_final
    else:
        return pd.DataFrame()  # Devolver un DataFrame vacío si no hay datos
    

# Ruta al archivo .pos
ruta_archivo = "temp.pos"

# Leer el archivo y generar el DataFrame
df_import = leer_archivo_pos(ruta_archivo)
df_import

# Limpieza de datos y correccion
df = df_import[["Iteracion","Elemento","Valor_1","Valor_2","Valor_3"]]
df = df.rename(columns={"Iteracion" : "Tiempo", "Valor_1" : "Temp_x", "Valor_2" : "Temp_y", "Valor_3" : "Temp_z"})
df = df.astype(float)
df["Tiempo"] = df["Tiempo"].astype(int)
df["Elemento"] = df["Elemento"].astype(int)
df["Temp_x"] = df["Temp_x"].round(2)-273
df["Temp_y"] = df["Temp_y"].round(2)-273
df["Temp_z"] = df["Temp_z"].round(2)-273

# modificacion de los elementos
df["Elemento"] = (df.index % 54340)+1

# Agregar columna promedio
df["Temp_mean"] = (df["Temp_x"]+df["Temp_y"]+df["Temp_z"])/3
df["Temp_mean"] = df["Temp_mean"].round(2)

max_mean = df["Temp_mean"].max()
print(f"Temperatura promedio maxima : {max_mean}")

#filas por iteracion
count = df["Tiempo"].value_counts().sort_index()

df_group = pd.DataFrame({"Temp_mean" : df["Temp_mean"].groupby(df.index // 54340).mean()}).reset_index(drop=True)
df_group["Tiempo"] = range(0,61)
df_group = df_group[["Tiempo", "Temp_mean"]]
df_group

df_temp_max = pd.DataFrame({"Temp_max" : df["Temp_mean"].groupby(df.index // 54340).max()}).reset_index(drop=True)
df_temp_max["Tiempo"] = range(0,61)
df_temp_max = df_temp_max[["Tiempo", "Temp_max"]]
df_temp_max

df_temp_max.to_csv('temperaturas_maximas.csv', index=False)
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

# Ruta y el nombre del archivo .xlsm
archivo_xlsm = ('PREDIC_SET.xlsm')

# Cargar el archivo .xlsm
workbook = load_workbook(archivo_xlsm, keep_vba=False)  # Establece keep_vba en False para eliminar las macros

# Guardar el archivo como .xlsx
archivo_xlsx = 'archivo.xlsx'
workbook.save(archivo_xlsx)

archivo_excel = 'C:\\Users\\User\\Desktop\\Programming\\Curves_pumps\\archivo.xlsx'
documento_base = pd.read_excel(archivo_excel, sheet_name= None)

## definir las hojas a eliminar
del documento_base['PREDICT'], documento_base['GRAFICAS Kwh-Bbl'], documento_base['BACKLOG 2022'], documento_base['PROTECCIONES MURPHY'], documento_base['Medida Fondo'], documento_base['VERSION SOFTWARE'], documento_base['PLAN DE ACCION EVACUADAS'], documento_base['Sheet2']

for key, hoja in documento_base.items():
    hoja.drop([0], inplace= True) #elimina la primera fila de datos
    hoja.insert(0, 'WELL', value= key)#insertar la columna con el nombre de cada pozo
    hoja.ffill(inplace=True) #rellenar los datos vacios con el numero anterior.

info_list = []
for info in documento_base.values():
    info_list.append(info)

print(type(info_list))
# print(info_list)

# Crear un dataframe a partir de lista de dataframes
dataframe1 = pd.concat(info_list, axis=0, ignore_index=True )

valor_a_eliminar = 'DESPUES DE INGRESAR LOS PRIMEROS DATOS BORRAR LAS CELDAS EN AMARILLO CON DELETE CELLS Y UP'
dataframe1 = dataframe1[dataframe1['FRECUENCIA'] != valor_a_eliminar]

valores_a_reemplazar = ['nd', 'NO', '1211-9', 'fds', '-', 'FDS', 'cñg8d', 'ND', ' - ', '0.86|', 
                        'SIN DATOS', 'sin datos', 'o.45', "299'", 'No lectura', 'No medido', 
                        'No registra', ' ']

for columna in dataframe1.columns:
    if columna == 'WELL' or columna == 'FECHA':
        continue  # Saltar a la siguiente columna si es de tipo 'datetime' o 'str'
    
    for indice, valor in dataframe1[columna].items():
        if isinstance(valor, str):
            # Reemplazar comas por puntos
            valor = valor.replace(',', '.')
            # Reemplazar "nd" por NaN
        if valor in valores_a_reemplazar:
            valor = 'NaN'
        dataframe1.at[indice, columna] = float(valor)
        
    if dataframe1[columna].dtype == 'object':
        dataframe1[columna] = dataframe1[columna].astype(float)

print(dataframe1) 

import pandas as pd
import plotly_express as px
from openpyxl import load_workbook

# # Ruta y el nombre del archivo .xlsm
# archivo_xlsm = ('PREDIC_SET.xlsm')

# # Cargar el archivo .xlsm
# workbook = load_workbook(archivo_xlsm, keep_vba=False)  # Establece keep_vba en False para eliminar las macros

# # Guardar el archivo como .xlsx
# archivo_xlsx = 'archivo.xlsx'
# workbook.save(archivo_xlsx)

# ####
# # la ruta del nuevo archivo Excel
# archivo_excel = 'archivo.xlsx'

# # leer el archivo Excel con pandas
# xl = pd.ExcelFile(archivo_excel)

# # Obtener una lista de nombres de hojas en el libro de Excel
# nombres_hojas = xl.sheet_names

# # Definir las hojas a mantener (las que NO se eliminaran)
# hojas_a_mantener = ['TRD-04', 'TRD-05', 'TRD-06', 'TRD-07', 'TRD-08', 'TRD-09', 'TRD-11', 
#                     'TRD-14', 'TRD-15', 'FLA-02', 'FLA-03', 'CGN-01', 'CGN-03', 'CGE-01', 'CNG-04', 
#                     'CNG-05', 'CNG-07', 'CÑG8D', 'BQA-03', 'LGL-04', 'LGL-05', 'LGL-07', 'LGL-14', 
#                     'LGL-15', 'LGL-16', 'LGL-17', 'LGL-18', 'LGL-19', 'LGL-20', 'LGN-04', 'LGN-06', 
#                     'MOR7', 'CAS-01', 'CAS-03', 'CAE-02', 'CAE-01', 'CHP-01', 'ABJ5', 'CHP-03', 'GSR-01', 
#                     'GSR-02', 'GSR-03', 'GRL-01', 'GRL-02', 'GRL-03', 'GRL-05', 'GRL-06', 'GRL-07', 'GRL-09', 
#                     'PRV-01', 'JRD-02', 'JRD-05', 'CDL-01', 'SAD-02', 'SAD-3A', 'SAD-06', 'SAD-07', 'SAD-09', 
#                     'SAD-10', 'ORO-05', 'ORO-07', 'ORO-08', 'VIR-03', 'CGL-01', 'CGL-05', 'RMN-03', 'RMN-05', 
#                     'RMN-07', 'RMS-02', 'CRN-01', 'CRS-01', 'CRN-02D', 'CRN-3H', 'CRV-01', 'CRV-01C', 'CRV-02', 
#                     'CRV-02A', 'CRV-05', 'CRV-05A', 'CRV-05B', 'CRV-05C', 'CRV-06A', 'CRV-06B', 'CRV-08', 'CRV-08A', 
#                     'CRV-08B', 'CRV-08C', 'CRV-10A', 'CRV-10B', 'CRV-10C', 'CRV-10D', 'CRV-CHNE', 'CAR-04', 'CAR-07', 
#                     'YAM-02', 'CHA-01', 'BAL-001', 'BAL-002D', 'BAL-004']  

# # Crear un objeto ExcelWriter para escribir el archivo Excel resultante
# with pd.ExcelWriter('archivo_resultante.xlsx', engine='openpyxl') as writer:
#     for hoja in nombres_hojas:
#         if hoja in hojas_a_mantener:
#             # Leer la hoja actual en un DataFrame
#             df = xl.parse(hoja)
            
#             # Escribir el DataFrame en el archivo Excel resultante
#             df.to_excel(writer, sheet_name=hoja, index=False)

#leer el archivo, pandas lo entrega como un diccionario, no como dataframe
# df = pd.read_excel("archivo_resultante.xlsx", sheet_name= None)

#pasar a df con el metodo concat
# df1 = pd.concat(df, axis=1)

#Metodo fillna para rellenar los valores faltantes (representados como None o NaN) con el valor 0
# df_filled = df1.fillna(0)

# df_prueba = df_filled['TRD-06']
#print(df_prueba.head(20))
#dtypes
# print(df_prueba.head(20))
#limpiar el df, retirar las letras 
#coger el titulo del pozo y pegarlo en una columna 
#unir los datos de todos los pozos en un solo dataframe
# fig = px.scatter(df_prueba, y='FECHA', x= 'PF OUT VSD')

#fig.show()
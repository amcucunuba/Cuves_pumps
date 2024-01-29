import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import load_workbook

def convertidor_xlsm_predictivos_a_xlsx (archivo_xlsm): 
# Cargar el archivo .xlsm
    workbook = load_workbook(archivo_xlsm, keep_vba=False)  # Establece keep_vba en False para eliminar las macros
# # Guardar el archivo como .xlsx
    archivo_nuevo_xlsx = 'archivo_2.xlsx'
    workbook.save(archivo_nuevo_xlsx)
    return

def convertidor_xlsx_predictivos_a_csv (archivo_xlsx):    
    documento_base = pd.read_excel(archivo_xlsx, sheet_name= None)
    ## definir las hojas a eliminar
    del documento_base['PREDICT'], documento_base['GRAFICAS Kwh-Bbl'], documento_base['BACKLOG 2022'], documento_base['PROTECCIONES Y TIEMPOS VSD'], documento_base['PROTECCIONES MURPHY'], documento_base['Medida Fondo'], documento_base['VERSION SOFTWARE'], documento_base['PLAN DE ACCION EVACUADAS'], documento_base['Sheet2'],
    # print(type(documento_base))
    for key, hoja in documento_base.items():
        if key == 'CNG-05':
            hoja.drop([1], inplace=True)
        hoja.drop([0], inplace= True) #elimina la primera fila de datos
        hoja.insert(0, 'WELL', value= key)#insertar la columna con el nombre de cada pozo
        hoja.bfill(inplace=True) #rellenar los datos vacios con el numero anterior.
        hoja.dropna(subset=['FECHA'], inplace=True)
    
    print(documento_base['JRD-05'])
    columnas = ['WELL','FECHA', 'FRECUENCIA', '% THD-VOL IN VSD', '% THD-AMP IN VSD',
        'PF IN VSD', '% THD-VOL OUT VSD', '% THD-AMP OUT VSD', 'PF OUT VSD',
        'VOL MTR A', 'VOL MTR B', 'VOL MTR C', 'VOL MTR A-Tierra',
        'VOL MTR B-Tierra', 'VOL MTR C-Tierra', '% THD-AMP MTR', 'PF MTR',
        'MAX VOL IN VSD', 'MAX AMP IN VSD', 'MAX VOL OUT VSD', 'RED KVA',
        '%RED KVA', 'RED KW', 'MAX AMP OUT VSD', '% LOAD VSD', 'KVA VSD',
        'KVA SUT', '% LOAD SUT', 'AMP MOTOR', '% LOAD MTR', '% DESB MTR',
        'VOL-A CON D', 'AMP-A CON D', 'VOL-B CON D', 'AMP-B CON D',
        'VOL-C CON D', 'AMP-C CON D', '%THD VOL CON D', '%THD AMP CON D',
        'P.F. CON D', 'VOL-A CON Y', 'AMP-A CON Y', 'VOL-B CON Y',
        'AMP-B CON Y', 'VOL-C CON Y', 'AMP-C CON Y', '%THD VOL CON Y',
        '%THD AMP CON Y', 'P.F. CON Y', 'PIP (psi)', 'T Motor (F)']

    for key, hoja in documento_base.items():
        if (col in hoja.columns for col in columnas):
            columnas_a_eliminar = [col for col in hoja.columns if col not in columnas]
            print (columnas_a_eliminar)
            hoja.drop(columns=columnas_a_eliminar, inplace=True)

    a_eliminar = ['Unnamed: 50', 'Unnamed: 51', 'Unnamed: 52',
                'FECHA.1', 'FRECUENCIA.1', 'BWPD', 'DIFERENCIA BOPD',
                'DIFERENCIA BWPD', 'BOPD', 'BFPD.1','Q. OIL','BFPD',
                'DIFERENCIA BFPD', '%BSW', '°API', 'NETOS', 'Q. WATER']
    for key, hoja in documento_base.items():
        columnas_a_eliminar = [col for col in a_eliminar if col in hoja.columns]
        hoja.drop(columns=columnas_a_eliminar, inplace=True)

    info_list = []
    for info in documento_base.values():
        info_list.append(info)

    # Crear un dataframe a partir de lista de dataframes
    dataframe1 = pd.concat(info_list, axis=0, ignore_index=True )
    # eliminar las filas vacias si hay mas de 3 
    dataframe1= dataframe1.dropna(thresh=4)
    print (dataframe1.iloc[1280:1330, :])

    dataframe1.set_index('FECHA', inplace=True)
    fechas_incorrectas = ['nd','19-11-22']
    dataframe1.drop(index=fechas_incorrectas, inplace= True)

    valor_a_eliminar = 'DESPUES DE INGRESAR LOS PRIMEROS DATOS BORRAR LAS CELDAS EN AMARILLO CON DELETE CELLS Y UP'
    dataframe1 = dataframe1[dataframe1['FRECUENCIA'] != valor_a_eliminar]
    dataframe1.to_csv('datos_predictivos_esp_prueve.csv')
    valores_a_reemplazar = ['nd','NO', '1211-9', 'fds', '-', 'FDS', 'cñg8d', 'ND', ' - ', '0.86|', 
                            'SIN DATOS', 'sin datos', 'o.45', "299'", 'No lectura', 'No medido', 
                            'No registra', '_', ' ', '                                       ',]

    for columna in dataframe1.columns:
        if columna == 'WELL' or columna == 'FECHA':
            continue  # Saltar a la siguiente columna si es de tipo 'datetime' o 'str'
        
        for indice, valor in dataframe1[columna].items():
            if isinstance(valor, str):
                # Reemplazar comas por puntos
                valor = valor.replace(',', '.')
                # Reemplazar "nd" por NaN
    
    dataframe1.replace(valores_a_reemplazar, np.nan, inplace=True)
            
    dataframe1 = dataframe1.apply(pd.to_numeric, errors='ignore')
    
    # print(dataframe1)
    dataframe1.reset_index(drop=False, inplace=True)
    dataframe1.to_csv('datos_predictivos_esp_2.csv')
    print (dataframe1.iloc[1280:1330, :])
    return  


if __name__ == '__main__' : 
    # print(convertidor_xlsm_predictivos_a_xlsx ('PREDIC_SET.xlsm'))
    # print(type(convertidor_xlsm_predictivos_a_xlsx ('PREDIC_SET.xlsm')))
    # convertidor_xlsm_predictivos_a_xlsx ('PREDIC_SET_2.xlsm')
    convertidor_xlsx_predictivos_a_csv ('archivo_2.xlsx')
    print('listo')
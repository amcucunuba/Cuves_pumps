import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
 

data_df = pd.read_csv('datos_predictivos_esp.csv')
data_df= data_df.round({'FRECUENCIA': 1, 
                   'PF OUT VSD': 2,
                   'PF IN VSD': 2, 
                   'VOL MTR A': 0, 
                   'VOL MTR B': 0, 
                   'VOL MTR C': 0,
                   'RED KVA': 1,
                   'RED KW': 1,
                   'KVA VSD': 1,
                   'KVA SUT': 1,
                   'AMP MOTOR': 0,
                   '% LOAD MTR': 1, 
                   'T Motor (F)': 0}, )


# for i in data_df['FECHA']:
#     # print (f'esto es i', i)
#     if isinstance(i, str):
#        aa = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
     
#     print(i)

# print(dataframe1.iloc[700:800, 0:6])

import pandas as pd
import datetime
from openpyxl import load_workbook
 

data_df = pd.read_csv("data/datos_predictivos_esp_2.csv")
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

data_df = data_df.dropna(subset=['FECHA'])
data_df['FECHA'] = pd.to_datetime(data_df['FECHA'])
data_df = data_df.sort_values(by='FECHA', ascending=False)

def compress(df, **kwargs):
    """
    Reduces the size of the DataFrame by downcasting numerical columns
    """
    input_size = df.memory_usage(index=True).sum()/ 1024**2
    print("old dataframe size: ", round(input_size,2), 'MB')

    in_size = df.memory_usage(index=True).sum()

    for t in ["float", "integer"]:
        l_cols = list(df.select_dtypes(include=t))

        for col in l_cols:
            df[col] = pd.to_numeric(df[col], downcast=t)

    out_size = df.memory_usage(index=True).sum()
    ratio = (1 - round(out_size / in_size, 2)) * 100

    print("optimized size by {} %".format(round(ratio,2)))
    print("new DataFrame size: ", round(out_size / 1024**2,2), " MB")

    return df

compress(data_df)
print(data_df.head(3))
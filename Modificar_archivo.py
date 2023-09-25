import pandas as pd

#leer el archivo, pandas lo entrega como un diccionario, no como dataframe
df = pd.read_excel("archivo.xlsx", sheet_name= None)
#pasar a df con el metodo concat
df1 = pd.concat(df, axis=1)

# print (df1)

## definir las hojas a eliminar 
hojas_eliminar = ['PREDICT', 'GRAFICAS Kwh-Bbl', 'BACKLOG 2022', 'PROTECCIONES MURPHY', 
                  'Medida Fondo','VERSION SOFTWARE', 'PLAN DE ACCION EVACUADAS']

for hoja in hojas_eliminar: 
    if hoja in df1.columns: 
        df1 = df1.drop(hoja, axis=1)


for hoja in df1:
    df1.insert(0, 'Name', value= df1.index)

print (df1)



import pandas as pd
import logging
import csv_generator as generador
import datetime

fecha = datetime.datetime.now()
dia = fecha.strftime("%d")
mes = fecha.strftime("%m")
ano = fecha.strftime("%Y")
fecha_de_hoy = ano + mes + dia + '.csv'


logging.basicConfig(
    filename = './SQLima.log',
    level = logging.DEBUG,
    filemode = 'w'
    )
logger = logging.getLogger()


generador.crear_csv(fecha_de_hoy)

df = pd.read_csv(fecha_de_hoy,delimiter=';')
#logging.info(df)
df.rename(columns=
{
    df.columns[0]:'fecha'
    ,df.columns[1]:'temperatura_maxima'
    ,df.columns[2]:'temperatura_minima'
    ,df.columns[3]:'ubicacion'
}
,inplace=True
)
df = df.groupby('ubicacion')['temperatura_maxima','temperatura_minima'].mean()
#logging.info(df.columns.values)
logging.info(df)
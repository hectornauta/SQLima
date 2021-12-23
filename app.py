import pandas as pd
import logging
import csv_generator as generador
import plotly.express as px

import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output

#Iniciamos la app de Dash
app = dash.Dash(__name__)

#Obtención de la fecha actual
fecha = datetime.datetime.now()
dia = fecha.strftime("%d")
mes = fecha.strftime("%m")
ano = fecha.strftime("%Y")
fecha_de_hoy = ano + mes + dia + '.csv'

#Inicialización del logger
logging.basicConfig(
    filename = './SQLima.log',
    level = logging.DEBUG,
    filemode = 'w'
    )
logger = logging.getLogger()

#Crear el csv limpiando el archjivo txt
generador.crear_csv(fecha_de_hoy)

#Importamos el CSV limpio y normalizado
df = pd.read_csv(fecha_de_hoy,delimiter=';')
df.rename(columns=
{
    df.columns[0]:'año'
    ,df.columns[1]:'mes'
    ,df.columns[2]:'dia'
    ,df.columns[3]:'temperatura_maxima'
    ,df.columns[4]:'temperatura_minima'
    ,df.columns[5]:'ubicacion'
}
,inplace=True
)
df[['año','mes','dia','temperatura_maxima','temperatura_minima']] = df[['año','mes','dia','temperatura_maxima','temperatura_minima']].apply(pd.to_numeric)

#Primer tipo de informe, promedio de temperaturas por ubicación
#Usar lista de keys para evitar warnings about deprecate cosas
dataframe_mes= df.groupby(['mes'])[['temperatura_maxima','temperatura_minima']].mean()
logging.info(dataframe_mes)
dataframe_mes.reset_index(inplace=True)

dff = dataframe_mes.copy()   
fig = px.scatter(
    data_frame=dff
    ,x = 'mes'
    ,y = ['temperatura_maxima','temperatura_minima']
)
fig.update_xaxes(type='category')

app.layout = html.Div([
    html.H1('Aplicación Web para visualiar datos meteorológicos de Argentina', style={'text-align':'center'}),
    html.Div(id='output_container',children=[]),
    html.Br(),
    dcc.Graph(id='Grafico',figure=fig)        
])
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
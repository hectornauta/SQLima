import logging
import csv_generator as generador

import datetime

import dash
import pandas as pd
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Inicialización del logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(module)s - %(message)s',
                    datefmt='%Y-%m-%d'
                    )
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

# Obtención de la fecha actual
# fecha = datetime.datetime.now()
# dia = fecha.strftime("%d")
# mes = fecha.strftime("%m")
# ano = fecha.strftime("%Y")
# fecha_de_hoy = ano + mes + dia + '.csv'

# Crear el csv limpiando el archjivo txt
# generador.crear_csv(fecha_de_hoy)

dataframe_provincias = pd.read_csv('PROVINCIAS.csv', delimiter=';')
dataframe_registros = pd.read_csv('REGISTROS.csv', delimiter=';')

provincias = dataframe_provincias['provincia']
provincias.drop_duplicates(inplace=True)
provincias.reset_index(drop=True, inplace=True)
lista_de_provincias = []
for provincia in provincias:
    lista_de_provincias.append(
        {'label': provincia, 'value': provincia}
    )

# Importamos el CSV limpio y normalizado
dataframe_registros.rename(columns={
    dataframe_registros.columns[0]: 'año',
    dataframe_registros.columns[1]: 'mes',
    dataframe_registros.columns[2]: 'dia',
    dataframe_registros.columns[3]: 'temperatura_maxima',
    dataframe_registros.columns[4]: 'temperatura_minima',
    dataframe_registros.columns[5]: 'ubicacion'},
    inplace=True
)
dataframe_registros[['año', 'mes', 'dia', 'temperatura_maxima', 'temperatura_minima']] = dataframe_registros[['año', 'mes', 'dia', 'temperatura_maxima', 'temperatura_minima']].apply(pd.to_numeric)
dataframe_registros = pd.merge(dataframe_registros, dataframe_provincias, on='ubicacion', how='inner')
logger.info(dataframe_registros)
# Primer tipo de informe, promedio de temperaturas por ubicación
# Usar lista de keys para evitar warnings about deprecate cosas
dataframe_mes = dataframe_registros.groupby(['provincia', 'mes'])[['temperatura_maxima', 'temperatura_minima']].mean()
logging.info(dataframe_mes)
dataframe_mes.reset_index(inplace=True)

# dataframe_mes_copia = dataframe_mes.copy()

# Iniciamos la app de Dash

app = dash.Dash(external_stylesheets=[dbc.themes.VAPOR])
app.layout = html.Div([
    html.Div([
        html.H1(
            "Informe meteorológico 2021",
            id="title",
            className="eight columns",
            style={"margin-left": "3%"},
        ),
        html.Img(
            src=('assets/nube.png'),
            className="two columns",
            id="nube-logo",
            style={'height': '5%', 'width': '5%'}
        )
    ], className="banner row"),
    html.Div([
        html.Div([
            html.P('Seleccione la provincia', className='fix_label', style={'color': 'black', 'margin-top': '2px'}),
            dcc.RadioItems(
                id='provincia-radioItems',
                labelStyle={'display': 'inline-block'},
                options=lista_de_provincias,
                value='Chaco',
                style={'text-align': 'center', 'color': 'black'}, className='dcc_compon'),
        ], className='create_container2 five columns', style={'margin-bottom': '20px'}),
    ], className='row flex-display'),
    html.Div([
        html.Div([
            dcc.Graph(id='line-graph', figure={})
        ], className='create_container2 eight columns'),
        html.Div([
            dcc.Graph(id='bar-graph', figure={})
        ], className='create_container2 five columns')
    ], className='row flex-display'),
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@app.callback(
    Output('line-graph', component_property='figure'),
    [Input('provincia-radioItems', component_property='value')]
)
def update_linegraph(value):
    dataframe_mes_filtro = dataframe_mes.drop(dataframe_mes.index[dataframe_mes['provincia'] != value])
    fig = px.line(
        data_frame=dataframe_mes_filtro,
        x='mes',
        y=['temperatura_maxima', 'temperatura_minima'],
        title='Promedio de temperaturas máximas y mínimas mensuales',
        markers=True,
        labels={'mes': 'Meses'}
    )
    fig.update_xaxes(type='category')
    newnames = {'temperatura_maxima': 'Temperatura Máxima', 'temperatura_minima': 'Temperatura Mínima'}
    fig.for_each_trace(
        lambda t: t.update(
            name=newnames[t.name],
            legendgroup=newnames[t.name],
            hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])
        )
    )
    fig.update_layout(
        yaxis_title="Temperaturas promedio",
        legend_title="Temperaturas"
    )
    fig.update_yaxes(range=[-50, 50])
    return fig

if __name__ == ('__main__'):
    app.run_server(debug=True)

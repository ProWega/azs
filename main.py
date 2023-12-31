from dash import Dash, html, dcc, callback, Output, Input, dash_table, ALL, Patch, callback


import pandas as pd
import sqlite3

import datetime
from datetime import date
import charts_utils

import dash_bootstrap_components as dbc

import data_utils
import flask

today = datetime.date.today()
# current_type_oil = db.oil_types_names[0]
# print(current_type_oil)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
# df = db.GetSingleDayDf(date(today.year, today.month, 24), current_type_oil)
# df.to_csv('test_delete.csv')
# data = GetDataPriceTableFromDB()
external_scripts = ['scripts/card.js']
app = Dash(__name__, assets_ignore='.*ignored.*', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.server.static_folder = 'static'
data_worker = data_utils.DataWorker()

wink_content = dbc.Card(
    dbc.CardBody(
        dcc.Graph(
            id='wink_last_update_main_bar',
            figure=charts_utils.GetWinkBarPlotLastUpdate()
        )
    )
)
independent_content = dbc.Card(
dbc.CardBody(
        dcc.Graph(
            id='independent_last_update_main_bar',
            figure=charts_utils.GetIndependentBarPlotLastUpdate()
        )
    )
)
all_companies_content = dbc.Card(
dbc.CardBody(
        dcc.Graph(
            id='all_companies_last_update_main_bar',
            figure=charts_utils.GetIndependentBarPlotLastUpdate()
        )
    )
)
azs_count = len(data_worker.main_df['Ссылка'].unique())
#last_refresh_date = data_utils.DateFromTimeStamp(data_worker.main_df['Дата'].values.max())
app.layout = html.Div([
    html.H1(children=f'Цены на топливо в Нижегородской области {data_utils.StringFromDate(pd.to_datetime(data_worker.max_date))} по {azs_count} АЗС', id='test'),
    dbc.Row(children=[
    dbc.Button([
                dbc.Row([

                    dbc.Col(children=[html.H5(children="Тип топлива")], md=3),
                    dbc.Col(children=[html.H5(children="Мин", className="price-value-main-page-card")],
                            md=3),
                    dbc.Col(children=[html.H5(children="Макс", className="price-value-main-page-card")],
                            md=3),
                    dbc.Col(children=[html.H5(children="Средн", className="price-value-main-page-card")],
                            md=3)

                ]),
            charts_utils.CreateFuelMainLInes()
        ], disabled=True, color='light')
    ], style={'margin': "20px"}),
    dbc.Row(children=[
        dbc.Tabs([
            dbc.Tab(wink_content, label='ВИНК компании'),
            dbc.Tab(independent_content, label='Независимые'),
            dbc.Tab(all_companies_content, label='Все компании')
        ]),

    ]),
    dbc.Row(children=[
    #charts_utils.CreateFuelMainLInes(),
    charts_utils.GetPriceDynamicAll()
    ])




    #charts_utils.CreateFuelLine(data_utils.oil_types_names[0], False),
    #charts_utils.CreateFuelLine(data_utils.oil_types_names[0], True)


])
def on_click_btn(n):
    print(n)
    return 'Ji' + str(n[0])

# Add controls to build the interaction


# @callback(Output(component_id='controls-and-graph', component_property='figure', allow_duplicate=True),
#          Input(component_id='my-date-picker-single', component_property='date'))
# def update_oil_prices(date):
#    df = db.GetSingleDayDf(date, current_type_oil)
'''

'''

if __name__ == '__main__':
    server = flask.Flask(__name__)
    app.run('0.0.0.0', server=server, debug=False)

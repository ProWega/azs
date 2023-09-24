from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import sqlite3
import DBworker
import datetime
from datetime import date

db = DBworker.DBparser()
today = datetime.date.today()
current_type_oil = db.oil_types_names[0]
print(current_type_oil)
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = db.GetSingleDayDf(date(today.year, today.month, 24), current_type_oil)
#df.to_csv('test_delete.csv')
# data = GetDataPriceTableFromDB()
app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Положение дел сегодня'),
    html.Hr(),
    dcc.RadioItems(options=db.oil_types_names, value=db.oil_types_names[0], inline=True, id='controls-and-radio-item'),
    #dcc.DatePickerSingle(
    #    id='my-date-picker-single',
    #    min_date_allowed=date(2023, 9, 24),
    #    max_date_allowed=date(2027, 9, 19),
    #    initial_visible_month=date(today.year, today.month, today.day),
    #   date=date(today.year, today.month, today.day)
    #),
    html.Div(id='output-container-date-picker-single'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6, sort_action='native', id='table'),
    dcc.Graph(figure={}, id='controls-and-graph')
])


# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    current_type_oil = col_chosen
    print(current_type_oil)
    df = db.GetSingleDayDf(date(2023, 9, 24), current_type_oil)
    fig = px.histogram(df, x='Тип топлива', y="Цена", histfunc='avg')
    return fig

@callback(Output(component_id='table', component_property='data'),
          Input(component_id='controls-and-radio-item', component_property='value')
)
def update_table(type_oil):
    df = db.GetSingleDayDf(date(today.year, today.month, 24), type_oil)
    return df.to_dict('records')




@callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    string_prefix = 'Цены на: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%d-%m-%Y')
        return string_prefix + date_string


#@callback(Output(component_id='controls-and-graph', component_property='figure', allow_duplicate=True),
#          Input(component_id='my-date-picker-single', component_property='date'))
#def update_oil_prices(date):
#    df = db.GetSingleDayDf(date, current_type_oil)


if __name__ == '__main__':
    app.run(debug=True)

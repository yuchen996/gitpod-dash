import dash
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output
import pandas as pd 
import numpy as np 
from dash import dash_table

df = pd.read_csv('https://raw.githubusercontent.com/sswatson/data/main/periodic-table.csv')
cols = df.columns

app = dash.Dash(__name__)

def identity(x):
    return x

# result1 = df.pivot_table(
#     index = value,
#     columns = 'dash_table',
#     aggfunc = np.sum
# )

app.layout = html.Div(children = [
    html.H1('Pivot table with identity functions'),

    html.H2('Row'),
    dcc.Dropdown(
        id='row',
        options=[{'label': i, 'value': i} for i in cols],
        value=cols[0]
    ),

    html.H2('Column'),
    dcc.Dropdown(id = 'col',
    options=[{'label': i, 'value':i} for i in cols],
    value = cols[1]
    ),

    html.H2('Value'),
    dcc.Dropdown(id = 'value',
    options=[{'label': i, 'value':i} for i in cols],
    value = cols[2]
    ),   

    html.H2('Result Table'),


    dash_table.DataTable(
        id = 'table',
        columns = [{"name": str(i), "id": str(i)} for i in df.columns],
    )
])

@app.callback([
    Output('table', 'data'),
    Output('table', 'columns')],
    [
    Input('row', 'value'),
    Input('col', 'value'),
    Input('value', 'value') 
    ]
)
 
def updateTable(row, col, v):

    tb = df.pivot_table(
        index = row,
        columns = col,
        values = v,
        aggfunc = identity
    )
    tb = pd.DataFrame(tb.to_records())
    tb_cols = [{'name':i, "id":i} for i in tb]
    return tb.to_dict('records'), tb_cols

if __name__ == '__main__':
    app.run_server(debug=True)
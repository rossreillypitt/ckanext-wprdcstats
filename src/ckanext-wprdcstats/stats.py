import csv

from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd

def csv_helper():
    with open("stats.csv", "r") as f:
        reader = csv.DictReader(f)
        raw_stats = [row for row in reader]
        raw_stats = change_raw_data(raw_stats)
        return raw_stats

def change_raw_data(raw_stats: list[dict[str, str | int | float]])->list[dict[str, str | int | float]]:
    year, month = '',''
    for row in raw_stats:
        for key, value in row.items():
            if key == '_id' or type(value) == int:
                continue
            if key == 'year_month':
                year, month = value.split('-')
            elif '.' in value:
                row[key] = float(value)
            else:
                row[key] = int(value)
        row['year'] = year
        row['month'] = month
    return raw_stats

rowData = csv_helper()
for row in rowData:
    row['unique_visitors'] = int(row['unique_visitors'])
columnDefs = [{'field': col_name} for col_name in rowData[0].keys()]
app = Dash()
df = pd.DataFrame(rowData)



x = [row['year_month'] for row in rowData]
y = [row['unique_visitors'] for row in rowData]


app.layout = [
    html.Div(children=["TAKE A LOOK A THIS"]),
    dcc.Graph(id='line'),
    dcc.Checklist(
        id='checklist',
        options=['2023', '2024', '2025', '2026'],
        value=['2023', '2024', '2025', '2026'],
        inline=True,
    )
]

@callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='checklist', component_property='value')
)
def update_graph(col_chosen):
    fig = px.line(x=x, y=y)
    return fig

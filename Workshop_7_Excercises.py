from dash import Dash, html, dash_table, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from faker import Faker
import random

app = Dash(__name__)

fake = Faker()
names = [fake.name() for _ in range(100)]
ages = [random.randint(18, 80) for _ in range(100)]
wins = [random.randint(0,82) for _ in range(100)]
wins.sort()

data = {'Name': names, 'Age': ages, 'Wins': wins}




df = pd.DataFrame(data)


dropdown_options = [
    {'label':'Age', 'value':'Age'},
    {'label':'Wins', 'value':'Wins'}
]


histogram_fig = px.histogram(df, x='Name', y='Age', title='Age Distribution by Name')



# Define the layout
app.layout = html.Div(
    children=[
        html.H1("Pandas DataFrame in Dash"),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_cell={
                'text-align': 'left',
                'whiteSpace':'normal',
                },
            style_header={
                'backgroundColor':'green',
                'fontWeight':'bold'
            },
            style_table={
                'overflowY':'scroll',
                'maxHeight':'300px'

            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'yellow',
                    'color':'black'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'black',
                    'color':'white'
                }
            ]
        ),
        dcc.Dropdown(
            id='dropdown-statistic',
            options = dropdown_options,
            value='Wins'
        ),
        dcc.Graph(
            id='statistics_graph'
        )
    ]
)

@app.callback(
    Output('statistics_graph', 'figure'),
    [Input('dropdown-statistic', 'value')]
)

def update_graph(selected_statistic):
    # Create the figure based on the selected statistic
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Name'],
        y=df[selected_statistic],
        marker_color='blue'
    ))
    fig.update_layout(
        title=f'{selected_statistic} Distribution by Name',
        xaxis_title='Name',
        yaxis_title=selected_statistic
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)


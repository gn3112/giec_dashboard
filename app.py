from enum import auto
from dash import Dash, html, dcc, Input, Output
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import dash_bootstrap_components as dbc

# Instantiate app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load dataset
df = pd.read_csv("Database_v0.csv", sep=";", decimal=",")
months = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']

print(df[months].max().max())

# Layout dashboard

fig = go.Figure(data=go.Scattergeo(
        # lon = df['long'],
        # lat = df['lat'],
        # text = df['text'],
        mode = 'markers',
        # marker_color = df['cnt'],
        ))

fig.update_layout(
        title = 'Map',
        geo_scope='europe',
    )

## Navigation bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Dashboard climat", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                dbc.Col(dbc.NavItem(dbc.NavLink("Mensuel", href="#main-container"))),
                dbc.Col(dbc.NavItem(dbc.NavLink("Comparaison", href="#my-slider")), width="auto"),
                ],
            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center"
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky="top"
)

# Main app layout
app.layout = html.Div(
    [
        navbar,
        html.Div([
        dcc.Dropdown(
            df["Ville"].sort_values(ascending=True), 
            df["Ville"][0],
            id="town-dropdown"
            ),
        dcc.Graph(
            id='line-plot-monthly',
        ),
        # dcc.Graph(figure=fig)
        dcc.Slider(0, 20, 5,
            value=10,
            id='my-slider',
            vertical=True
    ),
    ], id="main-container")
    ])

# Callbacks
@app.callback(
    Output('line-plot-monthly', 'figure'),
    Input('town-dropdown', 'value'))
def update_output(value):
    df_town = df[df["Ville"] == value][months].transpose()
    df_town.columns = ["temp"]

    selector_precip = [month + "P" for month in months]
    df_town2 = df[df["Ville"] == value][selector_precip].transpose()
    df_town2.columns = ["precip"]
    df_town2 = df_town2.rename(index=lambda s: s[:-1])

    new_df = df_town.join(df_town2)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
                x=new_df.index, 
                y=new_df["temp"],
                name="Temperature (°C)"
                ),
                secondary_y=False
    )
    

    fig.update_yaxes(range=[df[months].min().min(), df[months].max().max()],secondary_y=False)
    fig.update_yaxes(range=[df[selector_precip].min().min(), df[selector_precip].max().max()],secondary_y=True)

    fig.add_trace(go.Bar(x=new_df.index, y=new_df['precip'],
                    name='Precipitation (mm)',
                    marker_color = 'blue',
                    opacity=0.4,
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=2),
                    secondary_y=True
    )
    fig.update_layout(plot_bgcolor="white")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

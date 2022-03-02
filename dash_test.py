from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

print(df.head(10))


app.layout = html.Div(children=[
    html.H1(children='Giec dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
    ),

    dcc.Slider(
        min=1,
        max=10,
        step=1,
        value=1,
        id='slider'
    ),

    dcc.Graph(
        id='example2',
    )
])

@app.callback(
    Output('example2', 'figure'),
    Output('example-graph', 'figure'),
    Input('slider', 'value'))
def update_output(value):
    print("avant", value)
    df["Amount"] = df["Amount"]*value
    print("apres",df)
    return px.line(data_frame=df, y=df["Amount"]), px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

if __name__ == '__main__':
    app.run_server(debug=True)

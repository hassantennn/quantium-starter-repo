import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Quantium Starter – Dash OK"),
    dcc.Input(id="a", type="number", value=6),
    dcc.Input(id="b", type="number", value=7),
    html.Button("Compute", id="btn"),
    html.Div(id="out")
])

@app.callback(Output("out","children"), Input("btn","n_clicks"), Input("a","value"), Input("b","value"))
def compute(n, a, b):
    if not n:
        return "Click Compute"
    try:
        return f"Product: {float(a)*float(b)}"
    except Exception:
        return "Enter valid numbers"

if __name__ == "__main__":
    app.run(debug=True)


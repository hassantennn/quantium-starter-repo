import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load processed CSV
df = pd.read_csv("data/processed/pink_morsel_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Dashboard", style={"textAlign": "center", "color": "#800080"}),

    html.Div([
        html.Label("Select Region:", style={"fontSize": "20px", "marginRight": "10px"}),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"}
            ],
            value="all",
            labelStyle={"display": "inline-block", "margin-right": "15px"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    dcc.Graph(id="sales-chart")
], style={"fontFamily": "Arial", "margin": "20px"})

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        title="Daily Sales of Pink Morsels",
        labels={"Sales": "Total Sales ($)", "Date": "Date"},
        markers=True
    )
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="red")
    fig.update_layout(title_x=0.5)
    return fig

if __name__ == "__main__":
    app.run(debug=True)

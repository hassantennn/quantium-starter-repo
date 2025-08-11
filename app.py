import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Load processed data
df = pd.read_csv("data/processed/pink_morsel_sales.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Create Dash app
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# Region dropdown options
regions = [{'label': r.title(), 'value': r} for r in sorted(df['Region'].unique())]

app.layout = html.Div([
    html.H1("Pink Morsel Sales Before & After 15 Jan 2021", style={"textAlign": "center"}),
    
    html.Label("Select Region:"),
    dcc.Dropdown(
        id="region-dropdown",
        options=[{'label': 'All Regions', 'value': 'all'}] + regions,
        value='all',
        clearable=False
    ),
    
    dcc.Graph(id="sales-line-chart")
])

@app.callback(
    dash.Output("sales-line-chart", "figure"),
    dash.Input("region-dropdown", "value")
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['Region'] == selected_region]
    
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

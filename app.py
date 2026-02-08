
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Load the data
# We assume process_data.py has been run and formatted_output.csv exists
csv_file_path = "formatted_output.csv"

# Check if file exists to prevent crash on immediate start if not filtered yet
if not os.path.exists(csv_file_path):
    print(f"Error: {csv_file_path} not found. Please run process_data.py first.")
    df = pd.DataFrame(columns=["sales", "date", "region"])
else:
    df = pd.read_csv(csv_file_path)
    df = df.sort_values(by="date")

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the visualization
fig = px.line(df, x="date", y="sales", title="Pink Morsel Sales Over Time")
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    title_x=0.5
)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children="Pink Morsel Sales Visualizer", style={'textAlign': 'center'}),

    html.Div(children='''
        Visualizing sales data for Pink Morsels across all regions.
    ''', style={'textAlign': 'center'}),

    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

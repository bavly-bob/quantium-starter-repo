
import os

import dash
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

csv_file_path = "formatted_output.csv"

if not os.path.exists(csv_file_path):
    print(f"Error: {csv_file_path} not found. Please run process_data.py first.")
    df = pd.DataFrame(columns=["sales", "date", "region"])
else:
    df = pd.read_csv(csv_file_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values(by="date")

app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualizer"


def build_figure(selected_region):
    if df.empty:
        fig = px.line(title="No sales data available")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            title_x=0.5,
            template="plotly_white",
        )
        return fig

    if selected_region == "all":
        filtered_df = df.copy()
        fig = px.line(
            filtered_df,
            x="date",
            y="sales",
            color="region",
            title="Pink Morsel Sales Across All Regions",
        )
    else:
        filtered_df = df[df["region"] == selected_region]
        fig = px.line(
            filtered_df,
            x="date",
            y="sales",
            title=f"Pink Morsel Sales in the {selected_region.title()} Region",
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        title_x=0.5,
        template="plotly_white",
        legend_title_text="Region",
        margin={"l": 40, "r": 40, "t": 90, "b": 50},
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.95)",
    )
    fig.update_traces(line={"width": 3})
    return fig


app.layout = html.Div(
    className="page-shell",
    children=[
        html.Div(
            className="dashboard-card",
            children=[
                html.H1(
                    "Pink Morsel Sales Visualizer",
                    className="page-title",
                ),
                html.P(
                    "Track regional trends in Pink Morsel sales over time.",
                    className="page-subtitle",
                ),
                html.Div(
                    className="radio-wrapper",
                    children=[
                        html.Label("Filter by region", className="radio-heading"),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            className="region-selector",
                            labelStyle={
                                "display": "inline-flex",
                                "alignItems": "center",
                                "marginRight": "12px",
                            },
                            inputStyle={"marginRight": "8px"},
                        ),
                    ],
                ),
                dcc.Graph(
                    id="sales-line-chart",
                    figure=build_figure("all"),
                    className="sales-chart",
                    config={"displayModeBar": False},
                ),
            ],
        )
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def update_sales_chart(selected_region):
    return build_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)

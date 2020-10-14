import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io
from dash.dependencies import Input, Output, State
import dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("sample_data.csv")

df.reset_index(inplace=True)
print(df[:5])

df_columns = df.columns

app.layout = html.Div([
    html.H1('Analytics Dashboard',style={'text-align':'center'}),
    html.Div([
    html.H5('Xaxis', className="four columns"),
    dcc.Dropdown(id="column-select1",
                options=[
                    {'label':i,'value':i} for i in df_columns if i != "index"],
                multi=False,
                value=df_columns[0],
                style={'width':"60%"}
                ),
    html.Br(),
    html.H6('Top Value Filter',style={'textAlign': 'left'}, className="four columns"),
    html.Label('*- 0 value shows all the values'),
    dcc.Input(
            id="top", type="number",
            debounce=True, placeholder="Debounce True",
            value=5
        ),
    ],className='four columns',),
    html.Div([
    html.H5('Type of Graph', className="four columns"),
    dcc.Dropdown(id="column-select2",
                options=[
                    {'label':"Bar",'value':"bar"},
                    {'label':"Pie",'value':"pie"}],
                multi=False,
                value="bar",
                style={'width':"60%"}
                ),
    ],className='four columns',),
    html.Div(id="output-container",children=[]),
    html.Br(),
    html.Div([
    dcc.Graph(id="my_first_dash_graph",figure={})
    ],className='twelve columns',)
])



@app.callback(
    Output('my_first_dash_graph', 'figure'),
    [Input('column-select1', 'value'),
    Input('column-select2', 'value'),
    Input('top', 'value')])
def update_figure(col,graph_type,top_val):
    if "Repetitive" in col:
        value_counts = df[df["Repetitive/Nonrepetitive"] == "Repetitive"][col].value_counts(dropna=True, sort=True)
    else:
        value_counts = df[col].value_counts(dropna=True, sort=True)
    # solution here
    df_val_counts = pd.DataFrame(value_counts)
    df_value_counts = df_val_counts.reset_index()
    df_value_counts.columns = ['Category', 'count_cat']
    if graph_type == "bar":
        if top_val > 0:
            fig = px.bar(df_value_counts[:top_val], x="Category", y="count_cat",text="count_cat",color="Category")
        else:
            fig = px.bar(df_value_counts, x="Category", y="count_cat",text="count_cat",color="Category")
        fig.update_layout(transition_duration=500,
        title=str(col)+" Distribution",
        xaxis_title=col,
        yaxis_title="Count",
        showlegend=False)
    elif graph_type == "pie":
        if top_val > 0:
            fig = px.pie(df_value_counts[:top_val], values="count_cat", names="Category",hole=0.4)
        else:
            fig = px.pie(df_value_counts, values="count_cat", names="Category",hole=0.4)
        fig.update_traces(textposition='outside', textinfo='label+text+percent')
        fig.update_layout(transition_duration=500,
        title=str(col)+" Distribution",
        showlegend=False)

    return fig

if __name__=='__main__':
    app.run_server(debug=True)

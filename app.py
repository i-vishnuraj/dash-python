import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime as dt
import io
from dash.dependencies import Input, Output, State
import dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

file_name = "sample_data.xlsx"

if "csv" in file_name:
    df = pd.read_csv(file_name)
elif "xls" in file_name:
    df = pd.read_excel(file_name)

df.reset_index(inplace=True)
#print(df[:5])

#Add a reference column
for i in range(1,len(df)+1):
    df["Row Id"] = i

#Capture datetime fields
df_datefields = [i for i in df.columns if np.issubdtype(df[i].dtype, np.datetime64)]

#Add new hourly and monthly fields
if len(df_datefields):
    for i in df_datefields:
        new_colmonth_name = i + "_Month"
        #print(new_colmonth_name)
        df[new_colmonth_name] = df[i].dt.strftime('%b %y')
        new_col_hour_name = i + "_Hour"
        df[new_col_hour_name] = df[i].dt.strftime('%H')

df_columns = df.columns

app.layout = html.Div([
    html.H2('Analytics Dashboard',style={'text-align':'center'}),
    html.Div([
    html.H6('X-axis', className="four columns"),
    dcc.Dropdown(id="column-select1",
                options=[
                    {'label':i,'value':i} for i in df_columns if i != "index"],
                multi=False,
                value=df_columns[0],
                style={'width':"60%"}
                ),
    html.Br(),
    html.Label('Top X Value Filter (*- 0 value shows all)',style={'textAlign': 'left'}, className="four columns"),
    dcc.Input(
            id="topx", type="number",
            debounce=True, placeholder="Debounce True",
            value=5
        ),
    html.Br(),
    html.Br(),
    html.H6('Y-axis', className="four columns"),
    dcc.Dropdown(id="column-select2",
                options=[
                    {'label':i,'value':i} for i in df_columns if i != "index" and type(i) != "object"],
                multi=False,
                value=df_columns[0],
                style={'width':"60%"}
                ),
    html.Br(),
    html.Label('Top Y Value Filter (*- 0 value shows all)',style={'textAlign': 'left'}, className="four columns"),
    dcc.Input(
            id="topy", type="number",
            debounce=True, placeholder="Debounce True",
            value=5
        ),
    ],className='four columns',),
    html.Div([
    html.H6('Type of Graph', className="four columns"),
    dcc.Dropdown(id="graph-select",
                options=[
                    {'label':"Bar",'value':"bar"},
                    {'label':"Pie",'value':"pie"},
                    {'label':"Heat Map",'value':"heatmap"}],
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
    [Input('column-select1', 'value'), Input('column-select2', 'value'),
    Input('graph-select', 'value'), Input('topx', 'value'), Input('topy', 'value')])
def update_figure(col1,col2,graph_type,topx_val,topy_val):
    if "Repetitive" in col1:
        value_counts = df[df["Repetitive/Nonrepetitive"] == "Repetitive"][col1].value_counts(dropna=True, sort=True)
        # if col2 == "":
        #     value_counts = df[df["Repetitive/Nonrepetitive"] == "Repetitive"][col1].value_counts(dropna=True, sort=True)
        if col2 != "":
            #value_counts = df[df["Repetitive/Nonrepetitive"] == "Repetitive"].groupby(col1)[col2].value_counts(dropna=True, sort=True)
            value_counts_pivot = pd.pivot_table(df[df["Repetitive/Nonrepetitive"] == "Repetitive"], index=[col1],columns=[col2], aggfunc='count', fill_value=0)['Row Id']
    else:
        value_counts = df[col1].value_counts(dropna=True, sort=True)
    # solution here
    df_val_counts = pd.DataFrame(value_counts)
    df_value_counts = df_val_counts.reset_index()
    df_value_counts.columns = ['Category', 'count_cat']
    if graph_type == "bar":
        if topx_val > 0:
            fig = px.bar(df_value_counts[:topx_val], x="Category", y="count_cat",text="count_cat",color="Category")
        else:
            fig = px.bar(df_value_counts, x="Category", y="count_cat",text="count_cat",color="Category")
        fig.update_layout(transition_duration=500,
        title=str(col1)+" Distribution",
        xaxis_title=col1,
        yaxis_title="Count",
        showlegend=False)
    elif graph_type == "pie":
        if topx_val > 0:
            fig = px.pie(df_value_counts[:topx_val], values="count_cat", names="Category",hole=0.4)
        else:
            fig = px.pie(df_value_counts, values="count_cat", names="Category",hole=0.4)
        fig.update_traces(textposition='outside', textinfo='label+text+percent')
        fig.update_layout(transition_duration=500,
        title=str(col1)+" Distribution",
        showlegend=False)
    elif graph_type == "heatmap":
        def df_to_plotly(df):
            return {'z': df.values.tolist(), 'x': df.columns.tolist(), 'y': df.index.tolist()}
        fig = go.Figure(data=go.Heatmap(df_to_plotly(value_counts_pivot)))
        #fig.show()
    return fig

if __name__=='__main__':
    app.run_server(debug=True,port="8010",host="127.0.0.1")

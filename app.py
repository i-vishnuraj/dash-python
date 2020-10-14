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

df = pd.read_excel("sample_data.xlsx")

df.reset_index(inplace=True)
print(df[:5])

df_columns = df.columns
# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')
#
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#         df_columns = df.columns
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date))
#     ])
app.layout = html.Div([
    html.H1('Analytics Dashboard',style={'text-align':'center'}),
    # html.Div([
    # dcc.Upload(
    #     id='upload-data',
    #     children=html.Div([
    #         'Drag and Drop or ',
    #         html.A('Select Files')
    #     ]),
    #     style={
    #         'width': '90%',
    #         'height': '60px',
    #         'lineHeight': '60px',
    #         'borderWidth': '1px',
    #         'borderStyle': 'dashed',
    #         'borderRadius': '5px',
    #         'textAlign': 'center',
    #         'margin': '10px'
    #     },
    #     # Allow multiple files to be uploaded
    #     multiple=False
    # ),
    # html.Div(id='output-data-upload'),
    # ]),
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



# @app.callback(Output('output-data-upload', 'children'),
#               [Input('upload-data', 'contents')],
#               [State('upload-data', 'filename'),
#                State('upload-data', 'last_modified')])
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children

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

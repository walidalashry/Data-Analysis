import dash 
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input,Output,State
import os
import json
from dateutil import parser


#set the directory
PATH = 'D:/AI_pro/Semseter 02/visual'
# PATH = 'C:/Users/ALI/3D Objects/visualization/project'
os.chdir(PATH)


#read data
df = pd.read_csv('P1-UK-Bank-Customers.csv')
df['Date Joined'] = pd.to_datetime(df['Date Joined']).dt.date
with open('Countries_(December_2017)_Boundaries_UK.geojson') as response:
    uk_countries=json.load(response)


#counts
M=0
F=0

app=dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
                    html.H2('UK Bank Customers Dashboard', style={'textAlign':'center', 'color':'green'}),
                    html.Div(children=[
                        html.Div([html.H1(children=f'Users: {M+F}', style={'textAlign': 'center','color': 'black'},id='t'),
                                  html.H3(children=f'Male: {M}'   , style={'textAlign': 'center','color': 'blue'},id='m'),
                                  html.H3(children=f'Female: {F}', style={'textAlign': 'center','color': 'red'},id='f'),
                        dcc.Graph(id='map',
                         )], 
                         className='three columns'),
                        html.Div([dcc.Graph(id='balance_hist',
                         ),dcc.Graph(id='age_hist',
                          )], className='six columns'),
                        html.Div([html.H4(children='Select balance range :'),dcc.RangeSlider(
                                        id='balance-slider',
                                        min=0,
                                        max=200001,
                                        step=5000,
                                        value=[df.Balance.min(),df.Balance.max()],
                                        tooltip={True:'bottom'},
                                        marks={str(i): '{}k'.format(i//1000) for i in range(0,200001,25000)}
                                        ),
                                 html.H4(children='Select age range :'),dcc.RangeSlider(
                                        id='age-slider',
                                        min=df.Age.min(),
                                        max=81,
                                        step=1,
                                        value=[df.Age.min(),df.Age.max()],
                                        tooltip={True:'bottom'},
                                        marks={str(i): '{}'.format(i) for i in range(df.Age.min(),81,5)}
                                        ), 

                                 html.H4(children='Select date range :'),dcc.DatePickerRange(
                                     id='date-range',
                                     start_date_placeholder_text="Start Period",
                                     end_date_placeholder_text="End Period",
                                     calendar_orientation='vertical',
                                     start_date=df['Date Joined'].min(),
                                     end_date=df['Date Joined'].max(),
                                     min_date_allowed=df['Date Joined'].min(),
                                     max_date_allowed=df['Date Joined'].max(),

                                 ),
                                 html.Button(id='submit', n_clicks=0, children='Apply'),
                                 html.Div(id='test',
                                            children='testing here'),
                                 dcc.Graph(id='pie',
                                  ),

                                        ]
                        
                        
                        , className='three columns')])
])

@app.callback(
    Output('test', 'children'),
    Output('t', 'children'),
    Output('m', 'children'),
    Output('f', 'children'),
    Output(component_id='map', component_property='figure'),
    Output(component_id='balance_hist', component_property='figure'),
    Output(component_id='age_hist', component_property='figure'),
    Output(component_id='pie', component_property='figure'),
    Input('submit', 'n_clicks'),
    State(component_id='balance-slider', component_property='value'),
    State(component_id='age-slider', component_property='value'),
    State(component_id='date-range', component_property='start_date'),
    State(component_id='date-range', component_property='end_date'),
)
def update_dash(n_clicks , balance, age, start_date, end_date):

    df_filtered = df.query(f'Balance >= {balance[0]} and Balance <= {balance[1]}')
    df_filtered = df_filtered.query(f'Age >= {age[0]} and Age <= {age[1]}')
    df_filtered = df_filtered[df_filtered["Date Joined"] >= parser.parse(start_date).date()]
    df_filtered = df_filtered[df_filtered["Date Joined"] <= parser.parse(end_date).date()]

    test = [f"""the button has been clicked {n_clicks} times""" ,html.Br(),
     'balance range',str(balance),html.Br(),
     'age range',str(age),html.Br(),
     'date range',str(start_date),'->',str(end_date)]

    #map
    df_count = df_filtered['Region'].value_counts()
    df_count = pd.DataFrame(df_count.reset_index())
    df_count.columns = ['Region', 'count']
    df_count['id'] = df_count['Region'].replace({'England':1, 'Wales':4,
                                                    'Northern Ireland':2,'Scotland':3 })
    fig_01 = px.choropleth_mapbox(df_count, locations="id", featureidkey='properties.objectid', geojson=uk_countries, color='count'
                            , hover_name='Region',
                            mapbox_style='white-bg', zoom=4.2, center = {"lat": 55, "lon": -4},
                            color_continuous_scale="Viridis",
                            range_color=(0, 2500),
                            labels='count',
                            height=750,
                            width=460,
                            )
    fig_01.update_layout(coloraxis_showscale=False)

    #histogram_01
    x0_b = np.array(df_filtered[df_filtered['Gender']=='Male']['Balance'])
    x1_b = np.array(df_filtered[df_filtered['Gender']=='Female']['Balance'])
    fig_02 = go.Figure()
    fig_02.add_trace(go.Histogram(
        x=x0_b,
        histnorm='percent',
        name='Male', # name used in legend and hover labels
        nbinsx=20,
    ))
    fig_02.add_trace(go.Histogram(
        x=x1_b,
        histnorm='percent',
        name='Female',
        nbinsx=20,
    ))

    fig_02.update_layout(
        title_text='% Customers balance per gender', # title of plot
        xaxis_title_text='Balance (Pounds)', # xaxis label
        yaxis_title_text='percent', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )

    #histogram_02
    x0_a = np.array(df_filtered[df_filtered['Gender']=='Male']['Age'])
    x1_a = np.array(df_filtered[df_filtered['Gender']=='Female']['Age'])
    fig_03 = go.Figure()
    fig_03.add_trace(go.Histogram(
        x=x0_a,
        histnorm='percent',
        name='Male', # name used in legend and hover labels
        nbinsx=10,
    ))
    fig_03.add_trace(go.Histogram(
        x=x1_a,
        histnorm='percent',
        name='Female',
        nbinsx=10,
    ))
    fig_03.update_layout(
        title_text='% Customers age per gender', # title of plot
        xaxis_title_text='Age', # xaxis label
        yaxis_title_text='percent', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )



    #pieChart
    df_count = df_filtered['Gender'].value_counts()
    df_count = pd.DataFrame(df_count.reset_index())
    df_count.columns = ['Gender', 'count']
    fig_pie = px.pie(df_count, names='Gender', values='count')

    M=len(x0_a)
    F=len(x1_a)

    return test, f'Users: {M+F}',f'Male: {M}',f'Female: {F}',  fig_01, fig_02, fig_03, fig_pie

app.run_server()
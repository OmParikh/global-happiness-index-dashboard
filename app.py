import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df=pd.read_csv("assets/2019.csv")

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout=dbc.Container([
    html.Div(className='app-header',children=[
        html.H1("World Happiness Index Dashboard", className='display-3')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {'label': 'Overall rank', 'value': 'Overall rank'},
                    {'label': 'Score', 'value': 'Score'},
                    {'label': 'GDP per capita', 'value': 'GDP per capita'},
                    {'label': 'Social support', 'value': 'Social support'},
                    {'label': 'Healthy life expectancy', 'value': 'Healthy life expectancy'},
                    {'label': 'Freedom to make life choices', 'value': 'Freedom to make life choices'},
                    {'label': 'Generosity', 'value': 'Generosity'},
                    {'label': 'Perceptions of corruption', 'value': 'Perceptions of corruption'},
                ], 
                value='Score',
                style={'width': '100%'}
            )
    ],width={'size':6,'offset':3}, className='dropdown-container'),
        
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='world-map'),width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='data-insights', className='data-insights'),
            html.Div(id='top-bottom-countries', className='top-bottom-countries') 
        ], width=8),
        dbc.Col([
            html.Div(id='country-details', className='country-details')
        ],width=4)
    ])
], fluid=True)

@app.callback(
    Output('world-map', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_world_map(metric):
    fig = px.choropleth(df, locations='Country or region', locationmode='country names', color=metric, hover_name='Country or region', color_continuous_scale=px.colors.sequential.Aggrnyl_r, title=f"World Happiness Index:{metric}")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('data-insights', 'children'),
    Input('metric-dropdown', 'value')
)
def update_data_insights(metric):
    highest=df.loc[df[metric].idxmax()]
    lowest=df.loc[df[metric].idxmin()]
    insights=[
        html.H3(f"Highest:{metric}: {highest['Country or region']}({highest[metric]})"),
        html.H3(f"Lowest:{metric}: {lowest['Country or region']}({lowest[metric]})")
    ]
    return insights

@app.callback(
    Output('top-bottom-countries', 'children'),
    Input('metric-dropdown', 'value')
)
def update_top_bottom_countries(metric):
    top_countries=df.nlargest(5, metric)
    bottom_countries=df.nsmallest(5, metric)
    top_countries_list=html.Ul([html.Li(f"{row['Country or region']}:{row[metric]}")
                                for _, row in top_countries.iterrows()])
    bottom_countries_list=html.Ul([html.Li(f"{row['Country or region']}:{row[metric]}")
                                for _, row in bottom_countries.iterrows()])
    return html.Div([
        html.Div([html.H3("Top 5 Countries"),top_countries_list], className='top-bottom-sections'),
        html.Div([html.H3("Bottom 5 Countries"),bottom_countries_list], className='top-bottom-sections'),
    ])

@app.callback(
    Output('country-details', 'children'),
    Input('world-map', 'clickData')
)
def update_country_details(clickData):
    if clickData:
        country_name=clickData['points'][0]['location']
        country_data=df[df['Country or region']==country_name]
        if not country_data.empty:
            country=country_data.iloc[0]
            details=[
                html.H3(f"Details for {country_name}"),
                html.P(f"Overall rank: {country['Overall rank']}"),
                html.P(f"Score: {country['Score']}"),
                html.P(f"GDP per capita: {country['GDP per capita']}"), 
                html.P(f"Social support: {country['Social support']}"),
                html.P(f"Healthy life expectancy: {country['Healthy life expectancy']}"),
                html.P(f"Freedom to make life choices: {country['Freedom to make life choices']}"),
                html.P(f"Generosity: {country['Generosity']}"),
                html.P(f"Perceptions of corruption: {country['Perceptions of corruption']}")           
                ]
            return html.Div(details, className='country-details-section')
    return html.Div("Select a country on the map", className='country-details-section')    
if __name__=="__main__":
    app.run_server(debug=True)
import dash  
import dash_core_components as dcc 
import dash_html_components as html
import dash_cytoscape as cyto 
import dash_table  
import plotly.graph_objs as go
import pandas as pd 
import numpy as np 
from datetime import datetime 
from datetime import timedelta  
import os 
import json   

# Tab CSS
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# style for title
titleStyle = {'textAlign': 'Center', 'fontSize':'3rem','background': '#EEFFDD'}

# Color
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# GET DATA 
df = pd.read_csv('./data/longform2.csv', index_col = 0)
dflong = df.iloc[:15, :]

dfhokkaido = df[df['area']=='北海道']
dfpergdp = df[df.item=='pergdp']
dffpergdp = dfpergdp[(dfpergdp.area == '北海道') | (dfpergdp.area == '東京都') | (dfpergdp.area=='千葉県') | (dfpergdp.area=='愛知県') | (dfpergdp.area=='大阪府') | (dfpergdp.area=='福岡県')]


dftable = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
dfcons = pd.read_csv('./data/jp_consumer2014.csv', index_col=0)
dfcons = dfcons.iloc[:10, :20]

#DATA FOR DATA11
dfmany = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')
available_indicators = dfmany['Indicator Name'].unique()

# DATA12
dfjpy = pd.read_csv('https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-web-trader/data/USDJPY.csv', index_col=1, parse_dates=['Date'])
dffjpy = dfjpy['2016/1/5']
dffjpy = dffjpy.resample('1S').last().bfill()

# cytoscape用データ   
nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20*lat, 'y': -20*long}
    }
    for short, label, long, lat in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

elements = nodes + edges



app = dash.Dash(__name__)

server = app.server 

app.layout = html.Div(children=[
    dcc.Tabs(id = "tabs-styled-with-inline", value='DATA1', 
    children=[

    # DATA1 
        dcc.Tab(label="DATA1", value='DATA1', style=tab_style, selected_style=tab_selected_style, 
            children=[
                html.Div([
                html.H1('The Power Of Data Visualization', 
                style={'marginTop': '10%',  'fontFamily': 'Arial Bold', 'textAlign': 'Center', 'fontSize': '4rem','color': 'limegreen'}),
                html.H1('With Dash!', style={'textAlign':'Center', 'fontFamily': 'Arial Bold', 'textAlign': 'Center', 'fontSize': '4rem','color': 'limegreen'})
                ],style = {'background': '#EEFFDD'}
                ),
                html.Div([
                    html.H1('20190405 大阪Pythonの会', style= {'marginRight': '2%',}),
                    html.H1('合同会社 長目　CEO  小川　英幸', style={'marginRight': '2%', })
                ], style={'marginTop':'15%', 'textAlign': 'right', 
                })
            ]),
    
    # DATA2
        dcc.Tab(label="DATA2", value='DATA2', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([
                    html.H3('自己紹介', style={'textAlign': 'Center', 'fontSize':'3rem','background': '#EEFFDD'}),
                    html.Div([
                    html.Img(src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190315/20190315143003.png" , style={'marginTop':'5%', 'marginLeft': '5%', 'display': 'inline-block', 'height': 500}),
                    html.Div([
                    html.H3('ひでやん'),
                    html.H3('@ogawahideyuki'),
                    html.H3('はんなりPythonの会、Crypto Kitchenのオーガナイザー'),
                    html.H3('合同会社 長目（ちょうもく）経営'),
                    html.H3('金融・データ・ブロックチェーンを扱う会社'),
                    html.H3('何事も全力でをモットーに')
                    ], style={'display': 'inline-block', 'fontSize': '2rem', 'marginLeft': '2%', 'color':'limegreen'})
                    ], style = {'background': '#EEFFDD'})
                ])
            ]),
    
    #DATA3
        dcc.Tab(label="DATA3", value='DATA3', style=tab_style, selected_style=tab_selected_style,
        children=[
            html.H3('Crypto Kitchenはじめました', style=titleStyle),
            html.Div([
                html.H3('ブロックチェーンの勉強会です  4/18木曜日　会場はここSOUさんです！'),
                html.Img(src='https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190403/20190403094253.png')]
            , style={'fontSize': '2rem', 'textAlign': 'Center','color':'limegreen', 'padding': '2%', 'background': '#EEFFDD'})
        ]
        ),

    #DATA4
        dcc.Tab(label="DATA4", value='DATA4', style=tab_style, selected_style=tab_selected_style,
        children=[
            html.H3('今日話すこと', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                    html.H3('１．データを見ることの重要性と問題点'),
                    html.H3('２．データをみんなで見るのにDash良いですよ'),
                    html.H3('３．じゃあそのDashってどうやって使うの？')
                ], style={'textAlign': 'Center', 'fontSize':'3rem', 'marginTop': '10%', 'background': '#EEFFDD', 'color':'limegreen'})
        ]),

    #DATA5
        dcc.Tab(label="DATA5", value="DATA5", style=tab_style, selected_style=tab_selected_style,
        children=[
            html.H3('データって何？', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                html.Img(src="https://cdn-ak.f.st-hatena.com/images/fotolife/m/mazarimono/20190315/20190315175525.png",style={'width': '25%', 'margin': '0 5% 0', 'display': 'inline'}),
                html.Div([
                html.H3('最近話題のこの本'),
                html.H3('事実に基づき世界を見る！'),
                html.H3('データを基に世界を正しく見る'),
                html.H3('データ == 事実')
                ], style={'display': 'inline-block', 'fontSize': '3rem', 'color': 'limegreen'}),
                ], style={'background': '#EEFFDD'}),
        ]),

    #DATA6
        dcc.Tab(label="DATA6", value="DATA6", style=tab_style, selected_style=tab_selected_style,
        children=[
                html.H3('データを見る?', style={'textAlign': 'Center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                html.Div([
                        dash_table.DataTable(
                            id = 'table1',
                            columns = [{"name": i, "id": i} for i in df.columns],
                            data = df[:500].to_dict("rows"),
                            sorting = True,

                        )
                ], style={'marginLeft':"15%", 'marginRight': '15%'})

        ]),

    #DATA7
        dcc.Tab(label="DATA7", value="DATA7", style=tab_style, selected_style=tab_selected_style,
        children=[
            html.Div([
                    html.H3('都道府県別一人当たりGDP')
                ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD'}),
                html.Div([
                dcc.Graph(
                    id='pergdpGraph',
                    figure={
                    'data': [
                        go.Scatter(
                            x = dffpergdp[dffpergdp['area'] == i]['year'],
                            y = dffpergdp[dffpergdp['area'] == i]['value'],
                            name = i,
                            mode = 'lines'
                        ) for i in dffpergdp.area.unique()
                    ],
                    'layout':go.Layout(
                        xaxis= {'title': '年度'},
                        yaxis= {'title': '一人当たりGDP'},
                        height = 700,
                    )
                }
                )
                ], style ={'height': '80%', 'background': '#EEFFDD'}),
                html.Div([
                dcc.Graph(
                    id='pergdpGraph2',
                    figure={
                    'data': [
                        go.Scatter(
                            x = dfpergdp[dfpergdp['area'] == i]['year'],
                            y = dfpergdp[dfpergdp['area'] == i]['value'],
                            name = i,
                            mode = 'lines'
                        ) for i in dfpergdp.area.unique()
                    ],
                    'layout':go.Layout(
                        xaxis= {'title': '年度'},
                        yaxis= {'title': '一人当たりGDP'},
                        height = 700,
                    )
                }
                )
                ], style ={'height': '80%', 'background': '#EEFFDD'}), 
                    ]),

    #DATA8
        dcc.Tab(label="DATA8", value="DATA8", style=tab_style, selected_style=tab_selected_style,
        children=[
                html.Div([
                    html.H3('データを情報化するときの問題点', style={'textAlign': 'center', 'fontSize':'3rem', 'background': '#EEFFDD'}),
                    html.Div([
                        html.H4('大量にデータがあっても見せれない(特にプレゼン)'),
                        html.H4('多くの意見を反映しにくい'),
                        html.H4('凄い発見も当たり前かのように見えてしまう'),

                    ], style = {'textAlign': 'Center', 'fontSize': '3rem', 'background': '#EEFFDD',
                    'color': 'limegreen', 'padding': '1%'})
        ])
        ]),

    #DATA9
        dcc.Tab(label="DATA9", value="DATA9", style=tab_style, selected_style=tab_selected_style,
        children=[
               html.H1('出来るよ！Dashなら！！', style={'textAlign': 'Center', 'fontSize': '4rem','marginTop': '15%', 'padding': '5%','background': '#EEFFDD', 'color': 'red'}) 
        ]),

    #DATA10
        dcc.Tab(label="DATA10", value="DATA10", style=tab_style, selected_style=tab_selected_style,
        children=[
            html.Div([
                        html.H3('都道府県別人口とGDP,一人当たりGDP', style={
                        'textAlign': 'center', 'fontSize':'2.5rem', 'background': '#EEFFDD'
                        }),
                    html.Div([
                    html.Div([
                        dcc.Graph(id = 'scatter-chart',
                        hoverData = {'points': [{'customdata': '大阪府'}]},
                        ),
                    dcc.Slider(
                        id = 'slider-one',
                        min = df['year'].min(),
                        max = df['year'].max(),
                        marks = {i: '{}'.format(i) for i in range(int(df['year'].min()), int(df['year'].max())) if i % 2 == 1},
                        value = 1955,
                        )
                        ], style={
                            'display': 'inline-block',
                            'width': '60%',
                            }),
                    html.Div([
                        dcc.Graph(id='chart-one'),
                        dcc.Graph(id='chart-two'),
                        dcc.Graph(id='chart-three'),
                    ],style={
                        'display': 'inline-block',
                        'width': '39%'
                        })
                    ], style={'background': '#EEFFDD', 'padding':'1%'}),
                    ])
        ]),


    #DATA11
        dcc.Tab(label="DATA11", value="DATA11", style=tab_style, selected_style=tab_selected_style,
        children=[
            html.Div([
                html.Div([
                    html.H3(['大量のデータを見ることも出来る！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                html.Div([
                        html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)'
                        ),
                    dcc.RadioItems(
                        id='crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                        )
                    ],
                    style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)'
                        ),
                    dcc.RadioItems(
                        id='crossfilter-yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                        )
                        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
                        ], style={
                            'borderBottom': 'thin lightgrey solid',
                            'backgroundColor': 'rgb(250, 250, 250)',
                            'padding': '10px 5px'
                        }),
                html.Div([
                html.Div([
                    dcc.Graph(
                        id='crossfilter-indicator-scatter',
                        hoverData={'points': [{'customdata': 'Japan'}]}
                        )
                        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
                    html.Div([
                        dcc.Graph(id='x-time-series'),
                        dcc.Graph(id='y-time-series'),
                        ], style={'display': 'inline-block', 'width': '49%'}),

                html.Div(dcc.Slider(
                    id='crossfilter-year--slider',
                    min=dfmany['Year'].min(),
                    max=dfmany['Year'].max(),
                    value=dfmany['Year'].max(),
                    marks={str(year): str(year) for year in dfmany['Year'].unique()}
                    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
                    ], style={'padding': '2%'}),
                    ], style = {'width': '80%', 'margin':'3% auto 3%', 'background': '#EEFFDD'})
                    ])
        ]),

    #DATA12
    dcc.Tab(label="DATA12", value="DATA12", style=tab_style, selected_style=tab_selected_style,
    children=[
        html.Div([
                html.Div([
                    html.H3(['ライブアップデートもできる！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                ]),
                html.Div([
                    dcc.Graph(id="usdjpy"),
                    dcc.Interval(
                        id = 'interval_components',
                        interval = 1000,
                        )
                ], style={'height': '30%', 'width': '80%', 'margin': '0 auto 0', 'textAlign': 'center','background': '#EEFFDD'}),
                ]),
            ]),

    #DATA13
    dcc.Tab(label="DATA13", value="DATA13", style=tab_style,            selected_style=tab_selected_style,
                children=[
                    html.Div([
                    html.Div([
                        html.H3(['グラフもいける！'], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'})
                        ]),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown-update-layout',
                            value='grid',
                            clearable=False,
                            options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                            ], style={'width': '30%', 'margin':'0 auto 0'}
                        ),
                        cyto.Cytoscape(
                            id='cytoscape-update-layout',
                            layout={'name': 'grid'},
                            style={'width': '80%', 'height': '700px', 'margin': '0 auto 0', 'padding': '5%'},
                            elements=elements
                            )
                        ]),
                    ]),
                ]),

    #DATA14
    dcc.Tab(label="DATA14", value="DATA14", style=tab_style,            selected_style=tab_selected_style,
    children=[
        html.Div([
                        html.H3('herokuで共有も簡単！')
                    ], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                    html.Div([
                        html.H3('Dashはウェブアプリケーション！！！'),
                        html.H3('hrokuに簡単に上げられる！！！'),
                        html.H3('方法は二つ！'),
                        html.H3('１．herokuにコマンドラインなどを使ってあげる'),
                        html.H3('２．herokuにgithubをつないで'),
                        html.H3('これにより、私のようなサーバー全然わからないみたいな人もウェブでデータを共有できる！'),
                        html.H3('2を使うと、みんなでgithubをいじりながら、ライブアップデートしてデータを見るようなことができる'),
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 50, 'color': 'limegreen', 'marginTop': '5%'})
    ]),

    #DATA15
    dcc.Tab(label="DATA15", value="DATA15", style=tab_style, selected_style=tab_selected_style,
    children=[
        html.Div([
                        html.H3('今日のまとめ')
                    ], style = {'textAlign': 'Center', 'fontSize': '2.5rem', 'background': '#EEFFDD', 'marginTop': '5%'}),
                    html.Div([
                        html.H3('このようにDashを使えば、かなりの量のデータを使った可視化が簡単にできる！'),
                        html.H3('これを使えば、これまで以上にデータから情報を得ることが可能になる！'),
                        html.H3('プレゼンテーションでも使えるのではないか？'),
                        html.H3('そのような使い方ができるのであれば、多くの意見が得られるようになり、これまでにないデータの活用ができる！'),
                        html.H3('注意'),
                        html.H3('Dashの最新のバージョンは0.40.0になっていますが、これを使ってherokuにアップすると、とんでもない表示になります。0.39.0を使いましょう！')
                    ], style = {'textAlign': 'Center', 'fontSize': '2rem', 'background': '#EEFFDD', 'padding': 50, 'color': 'limegreen', 'marginTop': '5%'})
    ])

    ])
])


# Back To DATA10
@app.callback(
    dash.dependencies.Output('scatter-chart', 'figure'),
    [dash.dependencies.Input('slider-one', 'value')]
)
def update_graph(selected_year):
    dff = df[df['year'] == selected_year]
    dffper = dff[dff['item']=='pergdp']
    dffgdp = dff[dff['item']== 'GDP']
    dffpop = dff[dff['item']== 'popu']

    return {
        'data': [go.Scatter(
            x = dffper[dffper['area']==i]['value'],
            y = dffgdp[dffgdp['area']==i]['value'],
            mode = 'markers',
            customdata = [i],
            marker={
                'size' : dffpop[dffpop['area']==i]['value']/100,
                'color': dffpop[dffpop['area']==i]['color'],
            }, 
            name=i,
        )for i in dff.area.unique()],
        'layout': {
            'height': 800,
            'title': '{}年の都道府県GDP、一人当たりGDP、人口（円の大きさ）'.format(selected_year),
            'paper_bgcolor': '#EEFFDD',
            'fontSize': "2rem",
            'xaxis': {
                'type': 'log',
                'title': '都道府県別一人当たりGDP(log scale)',
                'range':[np.log(80), np.log(1200)]
            },
            'yaxis': {
                'type':'log',
                'title': '都道府県別GDP(log scale)',
                'range':[np.log(80), np.log(8000)]
            },
            'hovermode': 'closest',
        }
    }

def create_smallChart(dff, area, name):
    return {
        'data':[go.Scatter(
            x = dff['year'],
            y = dff['value']
        )],
        'layout':{
            'height': 300,
            'title': '{}の{}データ'.format(area, name),
            'paper_bgcolor': '#EEFFDD',
        }
    }



@app.callback(
    dash.dependencies.Output('chart-one', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'GDP']
    return create_smallChart(dff, areaName, 'GDP')

@app.callback(
    dash.dependencies.Output('chart-two', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createPerGDP(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'pergdp']
    return create_smallChart(dff, areaName, 'pergdp')

@app.callback(
    dash.dependencies.Output('chart-three', 'figure'),
    [(dash.dependencies.Input('scatter-chart', 'hoverData'))]
)
def createPopu(hoverdata):
    areaName = hoverdata['points'][0]['customdata']
    dff = df[df['area']==areaName]
    dff = dff[dff['item'] == 'popu']
    return create_smallChart(dff, areaName, 'popu')


# Back To DATA11

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dffmany = dfmany[dfmany['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dffmany[dffmany['Indicator Name'] == xaxis_column_name]['Value'],
            y=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Value'],
            text=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dffmany[dffmany['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dffmany, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dffmany['Year'],
            y=dffmany['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dffmany = dfmany[dfmany['Country Name'] == country_name]
    dffmany = dffmany[dffmany['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dffmany, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dffmany = dfmany[dfmany['Country Name'] == hoverData['points'][0]['customdata']]
    dffmany = dffmany[dffmany['Indicator Name'] == yaxis_column_name]
    return create_time_series(dffmany, axis_type, yaxis_column_name)

# DATA12
# RealTime Graph usd-jpy
@app.callback(
    dash.dependencies.Output('usdjpy', 'figure'),
    [dash.dependencies.Input('interval_components', 'n_intervals')]
)
def update_graph(n):
    t = datetime.now()
    nowHour = t.hour
    nowMinute = t.minute 
    nowSecond = t.second 

    d = datetime(2016, 1, 5, nowHour+9, nowMinute, nowSecond)
    period = timedelta(seconds = 120)
    d1 = d - period 
    dffjpy1 = dffjpy.loc['{}'.format(d1): '{}'.format(d), :]

    return {
        'data': [go.Scatter(
            x = dffjpy1.index,
            y = dffjpy1['Bid']
        )],
        'layout':{
            'height': 600,
            'title': 'USD-JPY 1Second Charts'
        }
    }

# CytoScape callback
@app.callback(dash.dependencies.Output('cytoscape-update-layout', 'layout'),
              [dash.dependencies.Input('dropdown-update-layout', 'value')])
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }

if __name__=='__main__':
    app.run_server(debug=True)

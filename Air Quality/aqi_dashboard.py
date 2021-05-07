import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('aqi.csv')
df_c = pd.read_excel('colorscale.xlsx')
index_list = df_c.index.values.tolist() 

#AQI colorscale
aqi_colorbar, aqi_min, aqi_max = dict(title='AQI'), df_c['category_value'].min(), df_c['category_value'].max()

aqi_colorscale = [[df_c.iloc[index_list_item]['category_value']/aqi_max
                 , df_c.iloc[index_list_item]['color']] for index_list_item in index_list]

#Layout
fig_layout_title = 'Salt Lake Air Quality October 2020 to March 2021'
show_legend_tf = True

aqi_types = [{'label':str(aqi_type), 'value':aqi_type} for aqi_type in df['ParameterName'].unique()]

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(id='aqi-types', options=aqi_types, value=df['ParameterName'].min()),
    dcc.Graph(id='graph')
])

@app.callback(Output('graph','figure'),
             [Input('aqi-types','value')])
def update_figure(aqi_type):             

    # DATA ONLY FOR SELECTED AQI TYPE FROM DROPDOWN
    filtered_df = df[df['ParameterName']==aqi_type]

    df_x, df_y, df_z = filtered_df['MonthObserved'], filtered_df['DayObserved'], filtered_df['AQI'] 

    #Heatmap
    data = [go.Heatmap(
        x = df_x,
        y = df_y,
        z = df_z,
        colorscale = aqi_colorscale,
        colorbar = aqi_colorbar,
        zmin = aqi_min, zmax = aqi_max)]    

    #Layout
    layout = go.Layout(title=fig_layout_title)    

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server()        
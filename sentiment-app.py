import dash_core_components as dcc
import dash_html_components as html
import dash
import os
import requests
from flask import Flask
from dash.dependencies import Input, Output,State

server = Flask(__name__)
app = dash.Dash(__name__,server = server)

app.layout = html.Div(children = [
    html.H3('Sentiment Analysis App'),
    html.P('The prediction is the output of Logistic Regression model with 87% Accuracy'),
    dcc.Input(id = 'input',type='text',placeholder='Enter Text'),
    html.Div(id='output')
    ])

@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='input',component_property='value')]
)
def take_input(input_data):
        if input_data:
           url = os.getenv('API_URL')
           myobj = {'text': input_data}
           x = requests.post(url, data = myobj).json()
           prediction,pos_value,neg_value = x.get('prediction'),x.get('pos_value'),x.get('neg_value')            
           return dcc.Graph(
                id = 'sentiment_graph',
                figure = {
                    'data':[{'x':['Positive','Negative'],'y':[pos_value,neg_value],'type':'bar'}],
                'layout':{
                    'title':f'The sentence has a {prediction} sentiment',
                    'xaxis':{'title':'Sentiment'},
                    'yaxis':{'title':'Percentage'},
                    'plot_bgcolor':'#111111',
                    'paper_bgcolor':'#111111',
                    'font':{'color':'#7FDBFF'}
            }
                }
            )

if __name__ == '__main__':
    app.run_server(debug=True)

#Import necessary packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pandasql import sqldf  #importing pandasql
pysqldf = lambda q: sqldf(q, globals()) #create first pysqldf to translate sql code into data frame
df = pd.read_csv('/Users/camapcon/Box Sync/MIS Capstone/CapstoneProject.csv') #get the chart csv
df1 = pd.read_excel('/Users/camapcon/Box Sync/MIS Capstone/CommunityPartner.xls')
df.head() #to see what the columns look like

def generate_table(dataframe, max_rows=10): #a function to design tables
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def create_sql(): #SQL creation
    Primary = """SELECT PrimaryMission, Count(Project_Name) as Count_Mission, Count(CommunityPartner) as CommPartner, Sum(UNOstudents) as StudentCount, Sum(TotalHours) as HourCount From df GROUP BY PrimaryMission""" #create a data frame using a SQL
    Primary_df = pysqldf(Primary)
    return Primary_df

app = dash.Dash('') #create a Dash app
available_indicators = df1.Primary.unique()
app.layout = html.Div([
    html.Div([
        html.H4('A summary report by Primary Missions')
    ]),
    html.Div(generate_table(create_sql())),
    html.Br(),
    html.Div([
        html.H4('Dataset filtered by Primary Missions')
    ]),    
    html.Div([
        dcc.Dropdown(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in available_indicators], 
            multi=False, placeholder='Filter by Primary Mission...'),
        html.Div(id='output-a')
    ])
])

@app.callback( #this callback is to create the result of the dropdown action
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('dropdown-a', 'value')])

def update_table(value): #update the table

    dff = df1.loc[df1['Primary'] == value]
    return generate_table(dff)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"}) 

if __name__ == '__main__':
    app.run_server()
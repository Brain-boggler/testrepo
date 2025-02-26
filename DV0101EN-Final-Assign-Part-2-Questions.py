#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={"textAlign": "left", "color": "#503D36", "font-size": 24}),  # Include style for title

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(id='dropdown-statistics',
                     options=dropdown_options,
                     placeholder='Select a report type',
                     style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'})
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(id='select-year',
                     options=[{'label': i, 'value': i} for i in year_list],
                     placeholder='Select a year',
                     value=None,  # Corrected value initialization
                     style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'})
    ]),

    html.Div([  # TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(select_statistics, input_year):
    if select_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

# TASK 2.5: Create and display graphs for Recession Report Statistics
        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Automobile Sales During Recession (Year-wise)")
        )

        # Plot 2: Average number of vehicles sold by vehicle type (Bar Chart)
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average Vehicle Sales by Type During Recession")
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Advertising Expenditure Share by Vehicle Type During Recession")
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales (Bar Chart)
        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='Unemployment_Rate',
                          y='Automobile_Sales',
                          color='Vehicle_Type',
                          labels={'Unemployment_Rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]

    

# TASK 2.6: Create and display graphs for Yearly Report Statistics
# Yearly Statistic Report Plots
# Check for Yearly Statistics.
elif input_year and select_statistics == 'Yearly Statistics':
    yearly_data = data[data['Year'] == input_year]

    # Plot 1: Yearly Automobile sales using a line chart for the whole period
    # Grouping data for plotting
    yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(
        figure=px.line(yas,
                       x='Year',
                       y='Automobile_Sales',
                       title="Yearly Automobile Sales Trend")
    )

    # Plot 2: Total Monthly Automobile sales using a line chart
    # Grouping data for plotting
    mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
    Y_chart2 = dcc.Graph(
        figure=px.line(mas,
                       x='Month',
                       y='Automobile_Sales',
                       title='Total Monthly Automobile Sales')
    )

    # Plot 3: Bar chart for average number of vehicles sold during the given year
    # Grouping data for plotting
    avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    Y_chart3 = dcc.Graph(
        figure=px.bar(avr_vdata,
                      x='Vehicle_Type',
                      y='Automobile_Sales',
                      title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year))
    )

    # Plot 4: Total Advertisement Expenditure for each vehicle type using a pie chart
    # Grouping data for plotting
    exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    Y_chart4 = dcc.Graph(
        figure=px.pie(exp_data,
                      values='Advertising_Expenditure',
                      names='Vehicle_Type',
                      title='Total Advertising Expenditure by Vehicle Type in {}'.format(input_year))
    )

    # Returning the graphs for displaying Yearly data
    return [
        html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
    ]
else:
    return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


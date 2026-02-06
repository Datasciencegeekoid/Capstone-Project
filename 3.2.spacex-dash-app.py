# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    placeholder="Select a Launch Site Here",
                                    value='ALL',  # Default value is set to 'ALL'
                                    searchable = True
                                ),

                                html.Br(),




                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

        html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(id='payload-slider',
            min=0, max=10000, step=1000,
            marks={0: '0',
                100: '100'},
            value=[min_payload, max_payload]),

        html.Br(),

        html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        success_count = (spacex_df.groupby('Launch Site')['class']
        .value_counts()
        .reset_index(name='count'))
        success_only = success_count[success_count['class'] == 1]
        fig = px.pie(success_only,
        values='count',
        names='Launch Site',
        title='Total Successes by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = filtered_df['class'].value_counts()
        fig = px.pie(
        values=success_count.values,
        names=['Failure (0)', 'Success (1)'],
        title=f'Success vs Failure for {entered_site}'
        
        )
        return fig


"""

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
"""

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))

def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        filtered_df2 = spacex_df
        title2='Scatter Plot of Payload Mass vs. Launch Outcome By Booster'
    else:
        filtered_df2 = spacex_df[spacex_df['Launch Site'] == entered_site]
        title2 = f"Scatter Plot of Launches for {entered_site}: Payload Mass vs. Launch Outcome By Booster"
    filtered_df2 = filtered_df2[ (filtered_df2['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df2['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(filtered_df2, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category', 
                     title = title2,         

        )
    return fig



# Run the app
if __name__ == '__main__':
    app.run()


"""
Which site has the largest successful launches?
   KSC LC - 39A
Which site has the highest launch success rate?
   CCAFS SLC-40 at 42.9% 9
Which payload range(s) has the highest launch success rate?
   Between 2k and 5.5k
Which payload range(s) has the lowest launch success rate?
   Between 5.5k and 10k
Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
launch success rate?
   Booster version FT has the highest launch success rate
"""


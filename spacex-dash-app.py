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

# Get unique launch site names
launch_sites = spacex_df['Launch Site'].unique()

options = [{'label': 'All Sites', 'value': 'ALL'}]

for site in launch_sites:
    options.append({'label': site, 'value': site})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),
                                    html.Br(),   
# TASK 2: Add a pie chart to show the total successful launches count for all sites
html.Div(html.H2('Launch Success Rate (All Sites)', style={'textAlign': 'center'})),
dcc.Graph(id='success-pie-chart'), 
    
html.Br(),

html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
dcc.RangeSlider(id='payload-slider',
        min=0, 
        max=10000, 
        step=1000,
        marks={i: f'{i} kg' for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload] 
    ),

    html.Br(), # Separator

    # TASK 4: Scatter chart container
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        # Case 1: ALL sites selected (New Requirement: Total Success Count by Site)
        
        # 1. Filter the entire DataFrame to include ONLY successful launches (class == 1)
        successful_launches_df = spacex_df[spacex_df['class'] == 1]
        
        # 2. Group the successful launches by 'Launch Site' and count them
        data = successful_launches_df.groupby('Launch Site').size().reset_index(name='Successful Launches')
        
        # 3. Create the pie chart showing the contribution of each site to the total success count
        fig = px.pie(
            data, 
            values='Successful Launches', 
            names='Launch Site', 
            title='Total Successful Launches Count by Site (All Sites)'
        )
        return fig
    
    else:
        # Case 2: A specific launch site is selected (Same as before: Success vs. Failure for one site)
        
        filtered_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = filtered_site_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        
        # Map the numerical class to descriptive names
        outcome_counts['Outcome'] = outcome_counts['class'].map({0: 'Failure', 1: 'Success'})

        # Create the pie chart for the specific site
        fig = px.pie(
            outcome_counts, 
            values='count', 
            names='Outcome', 
            title=f'Launch Success vs. Failure for Site: {entered_site}',
            color='Outcome', 
            color_discrete_map={'Success': 'green', 'Failure': 'red'}
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider):
    filtered_df = spacex_df[
        (slider[0] <= spacex_df['Payload Mass (kg)']) & (spacex_df['Payload Mass (kg)'] <= slider[1])
    ]
    if entered_site == 'ALL':
        return px.scatter(filtered_df,
                          x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Launch Success Rate For All Sites')
    # return the outcomes in pie chart for a selected site
    filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    filtered_df['outcome'] = filtered_df['class'].apply(lambda x: 'Success' if (x == 1) else 'Failure')
    filtered_df['counts'] = 1
    return px.scatter (filtered_df,
                       x='Payload Mass (kg)', y='class',
                       color='Booster Version Category',
                       title='Launch Success Rate For ' + entered_site)

# Run the app
if __name__ == '__main__':
    app.run()

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from pymongo import MongoClient
import pandas as pd

app = Dash(__name__)

# Function to fetch the latest data from MongoDB
def fetch_latest_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['user']
    collection = db["user_information"]
    data_from_mongo = list(collection.find())
    df = pd.DataFrame(data_from_mongo)
    return df

# Initial data fetch
df = fetch_latest_data()

# Graphs
def create_graphs():
    # Graph 1: Nombre d'utilisateurs par nationalité
    nationality_counts = df['nationality'].value_counts().reset_index()
    nationality_counts.columns = ['nationality', 'count']
    fig1 = px.bar(nationality_counts, x='nationality', y='count', title='Nombre d\'utilisateurs par nationalité')

    # Graph 2: Histogram of Âge moyen des utilisateurs by gender
    fig2 = px.histogram(df, x='age', color='gender', marginal='box', title='Histogram of Âge moyen des utilisateurs by gender')
    fig2.update_xaxes(title_text='Âge moyen')
    fig2.update_yaxes(title_text='Count')

    # Graph 3: Domaines de courriel les plus courants
    email_domain_counts = df['domain_email'].value_counts().reset_index()
    email_domain_counts.columns = ['Domain', 'Count']
    fig3 = px.bar(email_domain_counts.head(10), x='Domain', y='Count', title='Domaines de courriel les plus courants')

    return fig1, fig2, fig3

# Layout
app.layout = html.Div([
    html.H1(children='Users Information', style={'textAlign': 'center'}),
    dcc.Graph(id='nat-gender-graph'),
    dcc.Graph(id='age-graph'),
    dcc.Graph(id='email-domain-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10000,  # Update every 10 seconds (adjust as needed)
        n_intervals=0
    )
])

# Callback to update the graphs at intervals
@app.callback(Output('nat-gender-graph', 'figure'),
              Output('age-graph', 'figure'),
              Output('email-domain-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graphs(n_intervals):
    global df
    df = fetch_latest_data()
    fig1, fig2, fig3 = create_graphs()
    return fig1, fig2, fig3

if __name__ == '__main__':
    app.run(debug=True)
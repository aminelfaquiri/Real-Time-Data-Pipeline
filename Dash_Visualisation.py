from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from pymongo import MongoClient
import pandas as pd

app = Dash(__name__)

# Connect to MongoDB and retrieve data
client = MongoClient("mongodb://localhost:27017/")
db = client['user']
collection = db["user_information"]
data_from_mongo = list(collection.find())
df = pd.DataFrame(data_from_mongo)

# Graph 1: Nombre d'utilisateurs par nationalité
nationality_counts = df['nationality'].value_counts().reset_index()
nationality_counts.columns = ['nationality', 'count']
fig1 = px.bar(nationality_counts, x='nationality', y='count', title='Nombre d\'utilisateurs par nationalité')

# Graph 2: Âge moyen des utilisateurs
fig2 = px.line(df, x='registered_date', y='age', title='Âge moyen des utilisateurs')
fig2.update_xaxes(title_text='Date d\'enregistrement')
fig2.update_yaxes(title_text='Âge moyen')

# Graph 3: Domaines de courriel les plus courants
email_domain_counts = df['domain_email'].value_counts().reset_index()
email_domain_counts.columns = ['Domain', 'Count']
fig3 = px.bar(email_domain_counts.head(10), x='Domain', y='Count', title='Domaines de courriel les plus courants')

app.layout = html.Div([
    html.H1(children='Users Information', style={'textAlign': 'center'}),
    dcc.Graph(id='nat-gender-graph', figure=fig1),
    dcc.Graph(id='age-graph', figure=fig2),
    dcc.Graph(id='email-domain-graph', figure=fig3),
])

if __name__ == '__main__':
    app.run(debug=True)

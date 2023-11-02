import json
import requests
import time

def data_genaretor():
    try:
        url = "https://randomuser.me/api/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()
        
        # Drop the sensitive data:
        data = data["results"][0]
        del data['login']
        del data['id']
        del data['phone']
        del data['cell']
        del data['picture']
        del data['location']['coordinates']
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {str(e)}")
        print("###########################")
        return None


print(data_genaretor())
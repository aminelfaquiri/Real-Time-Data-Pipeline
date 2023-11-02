import time 
import json 
import random 
from datetime import datetime
from user_generatore import data_genaretor
from kafka import KafkaProducer

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

data = {'gender': 'female', 'name': {'title': 'Miss', 'first': 'Oya', 'last': 'Mertoğlu'}, 'location': {'street': {'number': 6333, 'name': 'Maçka Cd'}, 'city': 'İzmir', 'state': 'İstanbul', 'country': 'Turkey', 'postcode': 80127, 'timezone': {'offset': '-12:00', 'description': 'Eniwetok, Kwajalein'}}, 'email': 'oya.mertoglu@example.com', 'dob': {'date': '1986-02-08T13:57:48.683Z', 'age': 37}, 'registered': {'date': '2016-01-21T06:57:31.876Z', 'age': 7}, 'nat': 'TR'}

# dummy_message = data_genaretor
if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    while True:

        data = data_genaretor()
        
        if data is not None:
            # Send the data to the 'messages' topic:
            print(f'Producing message @ {datetime.now()} | Message = {str(data)}')
            print("###########################")
            producer.send('messages', data)
        else :
            print("API request failed. Skipping this iteration.")
        
        time.sleep(10)
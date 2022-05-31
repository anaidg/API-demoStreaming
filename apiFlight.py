import requests
import json
from time import sleep

# AVIATION API parameters
access_key = "de81fd2245213cfd0f67f69549abf562"
limit = "100"
flight_status = "active"
arr_iata = "BCN"

aviation_url = "http://api.aviationstack.com/v1/flights" + \
            "?access_key=" + access_key + \
            "&flight_status=" + flight_status + \
            "&arr_iata=" + arr_iata
            # "&limit=" + limit  

# Power BI API Parameters
powerbi_api_url = "https://api.powerbi.com/beta/f260df36-bc43-424c-8f44-c85226657b01/datasets/d684339e-da1f-4216-8518-4d72cc0623ef/rows?tenant=f260df36-bc43-424c-8f44-c85226657b01&UPN=diana.milena.toro.arrieta%40kyndryl.com&key=SGwjy%2BPrtuCyKQc28rGzCumq3ZsAce4YlWXDYkQR5c%2FjVJKn8MF%2BgZVINZrVKa1UvrfZJM%2Br%2Bu5dmeaui5mzWg%3D%3D"

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

# Main code
while True:
    # Get all flights
    response = requests.get(aviation_url)

    if response.status_code != 200:
        print("Algo ocurrió. ERROR: ", response.status_code)
        print(response.json)
        exit()

    json_text = response.text

    python_obj = json.loads(json_text)

    data_array = []
    for flight in python_obj['data']:
        data = {}

        # Only flight in the air
        if flight['live'] != None:

            data['vuelo'] = flight['flight']['iata']
            data['aerolinea'] = flight['airline']['name']
            data['fecha_vuelo'] = flight['flight_date']
            data['origen'] = flight['departure']['airport']
            data['destino'] = flight['arrival']['airport']           
            data['latitud'] = flight['live']['latitude']
            data['longitud'] = flight['live']['longitude']
            data['altitud'] = flight['live']['altitude']
            data['velocidad'] = flight['live']['speed_horizontal']
            data['timestamp'] = flight['live']['updated']

            print("Enviando información del vuelo " + data['vuelo'])
            data_array.append(data)

    print("\nEnviando array: ")
    print(data_array)
    x = requests.post(powerbi_api_url, data = json.dumps(data_array), headers = headers)
    print("Status code: ",   x.status_code, " - Respuesta: ", x.text)
    print("\n")

    # Wait till next refresh    
    sleep(5)
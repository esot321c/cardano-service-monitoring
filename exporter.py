import requests
import time
from prometheus_client import start_http_server, Gauge

latest_slot_api1 = Gauge('latest_slot_api1', 'Latest slot from API 1')
latest_slot_api2 = Gauge('latest_slot_api2', 'Latest slot from API 2')
slot_difference = Gauge('slot_difference', 'Difference between API 1 and API 2 slots')

def fetch_api_data():
    try:
        response1 = requests.get('http://localhost:8080/block/latest')
        data1 = response1.json()
        slot1 = int(data1.get('slot', 0))
    except Exception as e:
        print(f"Error fetching data from API 1: {e}")
        slot1 = 0

    try:
        response2 = requests.get('https://api.beta.explorer.cardano.org/api/v1/blocks?page=0&size=1&sort=')
        data2 = response2.json()
        slot2 = int(data2['data'][0]['slotNo']) if data2.get('data') else 0
    except Exception as e:
        print(f"Error fetching data from API 2: {e}")
        slot2 = 0

    latest_slot_api1.set(slot1)
    latest_slot_api2.set(slot2)
    slot_difference.set(slot2 - slot1)

    # Print the data for debugging
    print(f"API 1 slot: {slot1}")
    print(f"API 2 slot: {slot2}")
    print(f"Slot difference: {slot2 - slot1}")

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        fetch_api_data()
        time.sleep(15)
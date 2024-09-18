This is a simple docker setup to run Prometheus and Grafana for monitoring a Cardano API, to ensure it is synced with the network. 

## Setup

1. Put the correct URL for your API on line 11 of exporter.py
2. Ensure the response fits the structure the exporter.py script expects, or change the script to match. 

The response from `block/latest` looks like this: 
```json
{
  "id":"cab624dd0539f159bc7d500e567e05ece8b495bcb805c5f879dd3cd9c3638e29",
  "number":"10852587",
  "slot":"135127061"
}
```

Note that line 13 of exporter.py get's the slot as follows: `slot1 = int(data1.get('slot', 0))`. If your API has a different response structure, change that line to get the slot properly. 

3. OPTIONAL: Change the external ports in the `docker-compose.yml` if they conflict with your in-use ports. 
4. Run `docker compose up -d`

## Grafana configuration

1. Navigate to the Grafana url (`localhost:3002` or whatever you set) and login with admin/admin. You may change the password at this time. 
2. Add Prometheus as a data source:
  a. Click on Connections in the left sidebar
  b. Select "Data sources"
  c. Click "Add data source"
  d. Choose "Prometheus"
  e. Set the URL to http://prometheus:9090 (or http://localhost:9090 if Prometheus is not in the same Docker network)
  f. Click "Save & Test" to ensure the connection is working
3. Create a new dashboard:
  a. Click the "+" icon in the top right
  b. Select "Dashboard"
  c. Click "Add visualization"
4. Configure the panel:
  a. In the query editor, select "Prometheus" as the data source
  b. Adjust the panel settings as needed (type of visualization, time range, etc.)
  c. Choose `slot_difference` as the metric. 
  d. Click "Apply" to add the panel to your dashboard
  e. OPTIONAL: Add more panels for `latest_slot_api1` and `latest_slot_api2` with "Stat" type of visualization
5. Save the dashboard: Click the save icon (💾) at the top of the dashboard and give it a name.
6. Set the timeframe of your choosing (Last 24 hours, for example), and make sure "auto" is selected under refresh frequency. 
7. Set up any alerts. Make sure they allow for a range of slot differences, as the API requests won't be perfectly in sync. -200 to 200 is generally enough. 
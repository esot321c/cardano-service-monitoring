This is a simple docker setup to run Prometheus and Grafana for monitoring a Cardano API, to ensure it is synced with the network. 

NOTE: rather than using localhost, you may have more success with a hardcoded IP. Anywhere you see `localhost` in this repo, it was tested using the network IP for the host machine. 

TODO: Add a .env for the port and url settings. 

## Setup

1. Put the correct URL for your API on line 11 of exporter.py
   
3. Ensure the response fits the structure the exporter.py script expects, or change the script to match. 

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
   
5. Run `docker compose up -d`

## Grafana configuration

1. Navigate to the Grafana url (`localhost:3002` or whatever you set) and login with admin/admin. You may change the password at this time.
   
2. Add Prometheus as a data source:
   
    - Click on Connections in the left sidebar
    - Select "Data sources"
    - Click "Add data source"
    - Choose "Prometheus"
    - Set the URL to `http://prometheus:9090` (or `http://localhost:9090` if Prometheus is not in the same Docker network)
    - Click "Save & Test" to ensure the connection is working
  
5. Create a new dashboard:
   
    - Click the "+" icon in the top right
    - Select "Dashboard"
    - Click "Add visualization"

7. Configure the panel:
   
    - In the query editor, select "Prometheus" as the data source
    - Adjust the panel settings as needed (type of visualization, time range, etc.)
    - Choose `slot_difference` as the metric. 
    - Click "Apply" to add the panel to your dashboard
    - OPTIONAL: Add more panels for `latest_slot_api1` and `latest_slot_api2` with "Stat" type of visualization
       
8. Save the dashboard: Click the save icon (💾) at the top of the dashboard and give it a name.
   
9. Set the timeframe of your choosing (Last 24 hours, for example), and make sure "auto" is selected under refresh frequency.
    
11. Set up any alerts. Make sure they allow for a range of slot differences, as the API requests won't be perfectly in sync. -200 to 200 is generally enough. 

## Troubleshooting

If you encounter issues with the metrics, you can try a few steps. `docker logs` for any of the services will be helpful, but you can also try the following steps:

1. Check Prometheus scraping:
   
    - Access Prometheus at `http://localhost:9090`
    - Go to Status > Targets to see if the `api_metrics` target is up and being scraped successfully
    - In the query box on the main page, try typing `latest_slot_api1` and hit Execute. If you see data, Prometheus is successfully collecting it.
      
3. Check Grafana setup:
   
    - Access Grafana at `http://localhost:3002`
    - Go to Configuration > Data Sources
    - Make sure Prometheus is added as a data source with the URL `http://prometheus:9090`
    - Test the connection to ensure Grafana can reach Prometheus
      
5. Create a panel in Grafana:
   
    - Create a new dashboard and add a panel
    - In the query editor, select Prometheus as the data source
    - Start typing latest_slot_api1 in the metric field, it should auto-complete if the metrics are available

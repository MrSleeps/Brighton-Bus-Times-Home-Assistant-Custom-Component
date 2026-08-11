"""Constants for the Brighton Bus Times integration."""

DOMAIN = "brighton_bus_times"

CONF_STOP_IDS = "stop_ids"
CONF_STOP_QUERY = "stop_name"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_BASE_URL = "https://brightonbustimes.uk"
DEFAULT_SCAN_INTERVAL = 30
MIN_SCAN_INTERVAL = 15
MAX_SCAN_INTERVAL = 300

API_PATH = "/api/home-assistant/departures"
STOPS_PATH = "/data/bus-map/stops.geojson"

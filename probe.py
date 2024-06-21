import requests
import urllib3
from requests.exceptions import ConnectionError
try:
    requests.get("https://serveo.net")
except urllib3.exceptions.MaxRetryError as e:
    print(f"Maximos retries excedidos: {e}")
except urllib3.exceptions.NewConnectionError as e:
    print(f"Error al conectar: {e}")
except ConnectionError as e:
    print(f"Error al conectar 2: {e}")
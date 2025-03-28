import requests

WHO_API_URL = "https://ghoapi.azureedge.net/api/Indicator"

def fetch_who_data():
    response = requests.get(WHO_API_URL)
    data = response.json()
    return data

if __name__ == "__main__":
    who_data = fetch_who_data()
    print(who_data)  # Print WHO dataset

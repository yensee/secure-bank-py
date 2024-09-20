import requests

# Fraud Detection API
def check_fraud_detection(transfer_data):
    response = requests.post("http://127.0.0.1:8000/check", json=transfer_data)
    if response.status_code == 200:
        return response.json().get("fraud", False)  # Assume the API returns `fraud: true/false`
    return True  # If the API fails, assume it is fraud to be safe

# Currency Exchange API
def get_exchange_rate(from_currency, to_currency):
    response = requests.get(f"https://currency-api.example.com/convert?from={from_currency}&to={to_currency}")
    if response.status_code == 200:
        return response.json().get("rate", 1.0)
    return None  # If API fails, return None

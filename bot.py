import requests
import json
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ARCHIVO = "eth_data.json"


def obtener_precio_22_marzo():
    url = "https://api.coingecko.com/api/v3/coins/ethereum/history"
    params = {"date": "22-03-2026"}
    data = requests.get(url, params=params).json()
    
    return data["market_data"]["current_price"]["usd"]


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})
    print(response.text)


def guardar(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=2)


def main():
    precio = obtener_precio_22_marzo()

    data = {
        "precio_base": precio
    }

    guardar(data)

    enviar_telegram(f"📌 Precio real del 22 marzo guardado: ${precio}")


if __name__ == "__main__":
    main()

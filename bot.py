import requests
from datetime import datetime
import json
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ARCHIVO = "eth_data.json"


def obtener_precio_eth():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ethereum", "vs_currencies": "usd"}
    return requests.get(url, params=params).json()["ethereum"]["usd"]


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})


def cargar():
    try:
        with open(ARCHIVO) as f:
            return json.load(f)
    except:
        return {}


def guardar(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=2)


def main():
    data = cargar()

    if "precio_base" not in data:
        enviar_telegram("❌ No hay precio base guardado")
        return

    precio_actual = obtener_precio_eth()
    precio_base = data["precio_base"]

    diferencia = precio_actual - precio_base
    porcentaje = (diferencia / precio_base) * 100

    # Determinar estado
    if precio_actual > precio_base:
        estado = "📈 SUBIÓ"
    elif precio_actual < precio_base:
        estado = "📉 BAJÓ"
    else:
        estado = "➖ IGUAL"

    mensaje = f"""
📊 ETH vs 22 Marzo

💰 Base (22 marzo): ${precio_base}
📅 Hoy: ${precio_actual}

{estado}
📊 Cambio: {round(porcentaje,2)}%
"""

    enviar_telegram(mensaje)


if __name__ == "__main__":
    main()

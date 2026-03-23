import requests
from datetime import datetime, timedelta
import json
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ARCHIVO = "eth_data.json"
FECHA_BASE = datetime(2026, 3, 22).date()
DIAS_SEGUIMIENTO = 15


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
    hoy = datetime.today().date()
    data = cargar()

    if hoy == FECHA_BASE and "precio_base" not in data:
        precio = obtener_precio_eth()

        data = {
            "precio_base": precio,
            "dias": 0,
            "inicio": str(hoy + timedelta(days=1))
        }

        guardar(data)

        enviar_telegram(f"📌 Precio base ETH: ${precio}")
        return

    if "precio_base" in data:
        if data["dias"] >= DIAS_SEGUIMIENTO:
            return

        inicio = datetime.fromisoformat(data["inicio"]).date()

        if hoy >= inicio:
            precio_actual = obtener_precio_eth()
            base = data["precio_base"]

            diff = precio_actual - base
            pct = (diff / base) * 100

            enviar_telegram(
                f"📊 Día {data['dias']+1}/15\n"
                f"Base: ${base}\n"
                f"Actual: ${precio_actual}\n"
                f"Cambio: {round(pct,2)}%"
            )

            data["dias"] += 1
            guardar(data)


if __name__ == "__main__":
    main()

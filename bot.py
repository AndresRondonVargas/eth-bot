def main():
    precio = obtener_precio_eth()

    data = {
        "precio_base": precio
    }

    guardar(data)

    enviar_telegram(f"📌 Precio base guardado (simulando 22 marzo): ${precio}")

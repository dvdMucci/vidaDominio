import os
import whois
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.text}")

def load_domains_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return []
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def check_domains(file_path):
    domains = load_domains_from_file(file_path)
    for domain in domains:
        try:
            domain_info = whois.whois(domain)
            expiration_date = domain_info.expiration_date

            # Algunos dominios pueden tener múltiples fechas de vencimiento
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]

            if expiration_date:
                today = datetime.now()
                days_to_expiry = (expiration_date - today).days

                if days_to_expiry == 30:
                    send_telegram_message(f"\ud83d\udea8 Aviso: El dominio {domain} vencer\u00e1 en 30 d\u00edas ({expiration_date.date()}).")
                elif days_to_expiry == 15:
                    send_telegram_message(f"\ud83d\udea8 Recordatorio: El dominio {domain} vencer\u00e1 en 15 d\u00edas ({expiration_date.date()}).")

        except Exception as e:
            print(f"Error al verificar el dominio {domain}: {e}")

if __name__ == "__main__":
    file_path = "dominios.txt"  # Ruta del archivo con los dominios
    check_domains(file_path)

import os
from dotenv import load_dotenv
import requests

# Carrega as variáveis do .env
load_dotenv()

def create_clickup_folder(client_name):
    """
    Cria uma pasta no ClickUp e retorna o ID da pasta criada.
    """
    space_id = os.getenv("SPACE_ID")
    api_key = os.getenv("CLICKUP_API_KEY")
    
    if not space_id or not api_key:
        print("SPACE_ID ou CLICKUP_API_KEY não configurados.")
        return None

    url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
    payload = {"name": client_name}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": api_key,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("id")
    except requests.RequestException as e:
        print(f"Erro ao criar pasta no ClickUp: {e}")
        return None

import os
from dotenv import load_dotenv
import requests

# Carregar variáveis do .env
load_dotenv()

def create_frameio_project(client_name):
    """
    Cria um projeto no Frame.io com as pastas 'Raw upload' e 'Final approval'.
    Retorna o ID do projeto criado.
    """
    team_id = os.getenv("FRAME_IO_TEAM_ID")
    api_key = os.getenv("FRAME_IO_API_KEY")
    
    if not team_id or not api_key:
        raise ValueError("As variáveis de ambiente FRAME_IO_TEAM_ID ou FRAME_IO_API_KEY não estão configuradas.")

    url = f"https://api.frame.io/v2/teams/{team_id}/projects"
    payload = {"name": client_name}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        # Criar projeto
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        project_data = response.json()
        project_id = project_data.get("id")
        if not project_id:
            raise Exception("ID do projeto não encontrado na resposta.")

        # Obter root_asset_id do projeto
        project_url = f"https://api.frame.io/v2/projects/{project_id}"
        project_response = requests.get(project_url, headers=headers)
        project_response.raise_for_status()
        root_asset_id = project_response.json().get("root_asset_id")
        if not root_asset_id:
            raise Exception("root_asset_id não encontrado.")

        # Criar pastas 'Raw upload' e 'Final approval'
        folder_url = f"https://api.frame.io/v2/assets/{root_asset_id}/children"
        create_folder(folder_url, headers, "Raw upload", project_id)
        final_folder_id = create_folder(folder_url, headers, "Final approval", project_id)

        return project_id, final_folder_id

    except requests.RequestException as e:
        print(f"Erro ao criar projeto no Frame.io: {e}")
        return None, None


def create_folder(folder_url, headers, folder_name, project_id):
    """
    Cria uma pasta em um projeto Frame.io.
    """
    payload = {"name": folder_name, "type": "folder", "project_id": project_id}
    response = requests.post(folder_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("id")

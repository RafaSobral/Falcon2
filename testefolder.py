import requests
import json

def create_folder_in_project():
    # Configurações
    project_id = "9fd5b16f-cdbf-46d4-ae2a-09b5811195e9"
    token = "fio-u-KCOIl1lTWtAsW5lQzWa7ohesowh3dPqOeNOYaUd0wZid_8a4UgXSWK1O04sd7VJv"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        # 1. Primeiro, verificar o projeto e obter root_asset_id
        project_url = f"https://api.frame.io/v2/projects/{project_id}"
        project_response = requests.get(project_url, headers=headers)
        project_response.raise_for_status()
        project_data = project_response.json()
        
        print("Informações do projeto:")
        print(json.dumps(project_data, indent=2))
        
        root_asset_id = project_data.get('root_asset_id')
        if not root_asset_id:
            raise Exception("root_asset_id não encontrado no projeto")

        print(f"\nroot_asset_id encontrado: {root_asset_id}")

        # 2. Criar pasta usando o root_asset_id
        folder_url = f"https://api.frame.io/v2/assets/{root_asset_id}/children"
        folder_payload = {
            "name": "Nova Pasta Teste",
            "type": "folder",
            "project_id": project_id
        }

        folder_response = requests.post(folder_url, json=folder_payload, headers=headers)
        folder_response.raise_for_status()
        folder_data = folder_response.json()

        print("\nPasta criada com sucesso:")
        print(json.dumps(folder_data, indent=2))
        
        return folder_data

    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP: {e}")
        print("Resposta do servidor:")
        print(json.dumps(e.response.json(), indent=2))
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

if __name__ == "__main__":
    result = create_folder_in_project()
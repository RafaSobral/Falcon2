import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Carregar variáveis do .env
load_dotenv()

def create_drive_folder(client_name, client_email):
    """
    Cria uma pasta no Google Drive e a compartilha com o email fornecido.
    """
    try:
        # Obter configurações do .env
        service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        parent_folder_id = os.getenv("GOOGLE_DRIVE_PARENT_FOLDER")
        
        if not service_account_file or not parent_folder_id:
            raise ValueError("As variáveis de ambiente necessárias não estão configuradas.")
        
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        # Criar a pasta
        file_metadata = {
            'name': client_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')

        # Compartilhar a pasta
        if client_email:
            permission = {'type': 'user', 'role': 'writer', 'emailAddress': client_email}
            service.permissions().create(fileId=folder_id, body=permission, sendNotificationEmail=True).execute()

        return folder_id
    except Exception as e:
        print(f"Erro ao criar pasta no Google Drive: {e}")
        return None

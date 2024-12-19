from google.oauth2 import service_account
from googleapiclient.discovery import build

def test_create_drive_folder(folder_name, email_to_share=None):
    """
    Testa a criação de uma pasta no Google Drive e compartilha com um email específico
    """
    try:
        # Configurações
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        SERVICE_ACCOUNT_FILE = r"C:\Users\Matheus\Documents\falcon\falcon-system\setup\falcon-file-system-1304bea1f282.json"
        
        # Autenticação
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        # Criar serviço
        service = build('drive', 'v3', credentials=credentials)
        
        # Metadata da pasta
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['1u8HYjvga0oZlM-fs8Rqu5MXXpjVSIHhC']  # Atualizado para o ID da nova pasta
        }

        # Criar pasta
        file = service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()

        folder_id = file.get('id')
        print(f"Pasta '{folder_name}' criada com sucesso!")
        print(f"ID da pasta: {folder_id}")

        # Compartilhar a pasta se um email foi fornecido
        if email_to_share:
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': email_to_share
            }
            
            service.permissions().create(
                fileId=folder_id,
                body=permission,
                sendNotificationEmail=True
            ).execute()
            
            print(f"Pasta compartilhada com {email_to_share}")

        return folder_id

    except Exception as e:
        print(f"Erro ao criar/compartilhar pasta: {e}")
        return None

if __name__ == "__main__":
    # Teste com um nome de pasta e email para compartilhar
    test_folder_name = "Pasta de Teste Python"
    email_to_share = "matheus.fdac@gmail.com"
    test_create_drive_folder(test_folder_name, email_to_share)

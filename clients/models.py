from django.db import models
from datetime import date
import requests
from django.utils.text import slugify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    client_name = models.CharField(max_length=255) 
    clickup_folder_id = models.CharField(max_length=255, blank=True, null=True)  
    frame_folder_id = models.CharField(max_length=255, blank=True, null=True) 
    is_active = models.BooleanField(default=True) 
    start_date = models.DateField(default=date.today, editable=True)  
    end_date = models.DateField(blank=True, null=True, editable=False)  
    final_approved_frame_folder = models.CharField(max_length=255, blank=True, null=True)  
    client_email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={
            'unique': 'A customer with this email is already registered.'
        }
    )
    custom_link = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    drive_folder_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        print("Chamando save() do modelo Client.")  # Log

        if not self.drive_folder_id:
            print("Criando pasta no Google Drive...")
            self.drive_folder_id = self.create_drive_folder()
            print(f"drive_folder_id retornado: {self.drive_folder_id}")
            
        if not self.frame_folder_id: 
            print("Criando pasta no Frame.io...")
            self.frame_folder_id = self.create_frameio_project()
            print(f"frame_folder_id retornado: {self.frame_folder_id}")
            
        if not self.clickup_folder_id:
            print("Criando pasta no ClickUp...")
            self.clickup_folder_id = self.create_clickup_folder()
            print(f"clickup_folder_id retornado: {self.clickup_folder_id}")
        
        # Define a data de término quando `is_active` for desmarcado
        if not self.is_active and self.end_date is None:
            self.end_date = date.today()
        elif self.is_active:
            self.end_date = None

        if not self.custom_link:
            self.custom_link = slugify(self.client_name)
        
        super(Client, self).save(*args, **kwargs)

    def create_frameio_project(self):
        """
        Cria um projeto no Frame.io com as pastas 'Raw upload' e 'Final approval'
        e retorna o ID do projeto criado.
        """
        team_id = "cc85cc50-09c7-42ab-8abb-136cec334e71" #teamID Letelba Neto
        url = f"https://api.frame.io/v2/teams/{team_id}/projects"
        payload = {
            "name": self.client_name 
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer fio-u-KCOIl1lTWtAsW5lQzWa7ohesowh3dPqOeNOYaUd0wZid_8a4UgXSWK1O04sd7VJv"
        }

        try:
            
            response = requests.post(url, json=payload, headers=headers)
            print(f"Resposta da API (criar projeto): {response.status_code}, {response.text}") 
            response.raise_for_status()
            project_data = response.json()
            project_id = project_data.get("id")
            
            if not project_id:
                raise Exception("ID do projeto não encontrado na resposta")

            
            project_url = f"https://api.frame.io/v2/projects/{project_id}"
            project_response = requests.get(project_url, headers=headers)
            project_response.raise_for_status()
            root_asset_id = project_response.json().get('root_asset_id')

            if not root_asset_id:
                raise Exception("root_asset_id não encontrado")

            
            folder_url = f"https://api.frame.io/v2/assets/{root_asset_id}/children"
            
           
            raw_payload = {
                "name": "Raw upload",
                "type": "folder",
                "project_id": project_id
            }
            raw_response = requests.post(folder_url, json=raw_payload, headers=headers)
            raw_response.raise_for_status()
            print(f"Pasta Raw upload criada: {raw_response.status_code}")

     
            final_payload = {
                "name": "Final approval",
                "type": "folder",
                "project_id": project_id
            }
            final_response = requests.post(folder_url, json=final_payload, headers=headers)
            final_response.raise_for_status()
            print(f"Pasta Final approval criada: {final_response.status_code}")
            
         
            final_folder_id = final_response.json().get('id')
            if final_folder_id:
             self.final_approved_frame_folder = final_folder_id
           
            
            return project_id

        except requests.RequestException as e:
            print(f"Erro ao criar projeto ou pastas no Frame.io: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None
        
    def create_clickup_folder(self):
        """
        Cria uma pasta no ClickUp e retorna o ID da pasta criada.
        """
        space_id = "90070241014"
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        payload = {
            "name": self.client_name
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "pk_82187560_FOKKW5MW9UWBXR4H6D1DLZ8AMOB5QKDJ"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Resposta da API ClickUp: {response.status_code}, {response.text}")
            response.raise_for_status()
            return response.json().get("id")
        except requests.RequestException as e:
            print(f"Erro ao criar pasta no ClickUp: {e}")
            return None
        
    def create_drive_folder(self):
        """
        Cria uma pasta no Google Drive e a compartilha com o email fornecido pelo cliente.
        """
        try:
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            SERVICE_ACCOUNT_FILE = r"C:\Users\Matheus\Documents\falcon\falcon-system\setup\falcon-file-system-1304bea1f282.json"
            
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
            service = build('drive', 'v3', credentials=credentials)
            
          
            file_metadata = {
                'name': self.client_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': ['1u8HYjvga0oZlM-fs8Rqu5MXXpjVSIHhC']  
            }

           
            file = service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            folder_id = file.get('id')
            print(f"Pasta criada com sucesso no Drive: {folder_id}")

     
            if self.client_email:
                permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': self.client_email
                }
                service.permissions().create(
                    fileId=folder_id,
                    body=permission,
                    sendNotificationEmail=True
                ).execute()
                print(f"Pasta compartilhada com {self.client_email}")

            return folder_id
        except Exception as e:
            print(f"Erro ao criar pasta no Google Drive: {e}")
            return None

    


class ClientUpload(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.client_name} - {self.file.name}"
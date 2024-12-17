from django.db import models
from datetime import date
import requests
from django.utils.text import slugify


class Client(models.Model):
    client_id = models.AutoField(primary_key=True) 
    client_name = models.CharField(max_length=255) 
    clickup_folder_id = models.CharField(max_length=255, blank=True, null=True)  
    frame_folder_id = models.CharField(max_length=255, blank=True, null=True) 
    is_active = models.BooleanField(default=True) 
    start_date = models.DateField(default=date.today, editable=False)  
    end_date = models.DateField(blank=True, null=True, editable=False)  
    final_approved_frame_folder = models.CharField(max_length=255, blank=True, null=True)  
    client_email = models.EmailField(max_length=255, blank=True, null=True) 
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    custom_link = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        print("Chamando save() do modelo Client.")  # Log para debug

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
        Cria um projeto no Frame.io e retorna o ID da pasta criada.
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
            print(f"Resposta da API: {response.status_code}, {response.text}") 
            response.raise_for_status()
            return response.json().get("id")
        except requests.RequestException as e:
            print(f"Erro ao criar projeto no Frame.io: {e}")
            return None

    def create_clickup_folder(self):
        """
        Cria uma pasta no ClickUp e retorna o ID da pasta criada.
        """
        space_id = "90070241014" # Substitua pelo ID do espaço correto
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        payload = {
            "name": self.client_name
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "pk_82187560_FOKKW5MW9UWBXR4H6D1DLZ8AMOB5QKDJ" # Substitua pelo token correto
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Resposta da API ClickUp: {response.status_code}, {response.text}")
            response.raise_for_status()
            return response.json().get("id")
        except requests.RequestException as e:
            print(f"Erro ao criar pasta no ClickUp: {e}")
            return None


class ClientUpload(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.client_name} - {self.file.name}"
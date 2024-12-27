from django.db import models
from datetime import date
from django.utils.text import slugify
import uuid
from clients.services.frameio_service import create_frameio_project
from clients.services.clickup_service import create_clickup_folder
from clients.services.drive_service import create_drive_folder
import random
import string

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
            self.drive_folder_id = create_drive_folder(self.client_name, self.client_email)
            print(f"drive_folder_id retornado: {self.drive_folder_id}")

        if not self.frame_folder_id:
            print("Criando projeto no Frame.io...")
            self.frame_folder_id, self.final_approved_frame_folder = create_frameio_project(self.client_name)
            print(f"frame_folder_id retornado: {self.frame_folder_id}")

        if not self.clickup_folder_id:
            print("Criando pasta no ClickUp...")
            self.clickup_folder_id = create_clickup_folder(self.client_name)
            print(f"clickup_folder_id retornado: {self.clickup_folder_id}")

        # Define a data de término quando `is_active` for desmarcado
        if not self.is_active and self.end_date is None:
            self.end_date = date.today()
        elif self.is_active:
            self.end_date = None

        if not self.custom_link:
            self.custom_link = slugify(self.client_name)

        super(Client, self).save(*args, **kwargs)


class ClientUpload(models.Model):
    raw_upload_id = models.CharField(
        max_length=18,
        editable=False,
        null=True  # Permite nulo temporariamente
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.client_name} - {self.file.name}"
    
    @staticmethod
    def generate_random_string(length=16):
        """Gera uma string aleatória de tamanho definido."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
from django.db import models
from datetime import date

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
        # Define a data de término quando `is_active` for desmarcado
        if not self.is_active and self.end_date is None:
            self.end_date = date.today()
        # Remove a data de término se `is_active` for marcado novamente
        elif self.is_active:
            self.end_date = None
        super(Client, self).save(*args, **kwargs) 

    def __str__(self):
        return self.client_name

class ClientUpload(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.client_name} - {self.file.name}"
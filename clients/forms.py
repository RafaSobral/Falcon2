from django import forms
from .models import Client, ClientUpload

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'client_name', 'clickup_folder_id', 'frame_folder_id', 
            'is_active', 'final_approved_frame_folder', 
            'client_email', 'client_phone'
        ]

class ClientUploadForm(forms.ModelForm):
    class Meta:
        model = ClientUpload
        fields = ['file']
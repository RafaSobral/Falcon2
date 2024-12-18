from django import forms
from .models import Client, ClientUpload

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['frame_folder_id', 'clickup_folder_id','final_approved_frame_folder', 'client_phone', 'is_active',  ]  
        fields = [
            'client_name', 'clickup_folder_id', 'frame_folder_id',
            'client_email', 'start_date',
        ]

class ClientUploadForm(forms.ModelForm):
    class Meta:
        model = ClientUpload
        fields = ['file']
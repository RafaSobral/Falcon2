from django.urls import path
from .views import ClientCreateView, check_client_email
from . import views

urlpatterns = [
    path('', ClientCreateView.as_view(), name='client-create'),  # Página principal será a criação de clientes
    path('upload/<slug:custom_link>/', views.upload_file, name='upload_file'),
    path('check-email/', check_client_email, name='check-client-email'),
]

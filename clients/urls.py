from django.urls import path
from .views import ClientCreateView
from . import views

urlpatterns = [
    path('', ClientCreateView.as_view(), name='client-create'),  # Página principal será a criação de clientes
    path('upload/<slug:custom_link>/', views.upload_file, name='upload_file'),
]

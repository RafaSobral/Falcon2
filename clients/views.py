from django.views.generic import CreateView
from .models import Client, ClientUpload 
from .forms import ClientForm, ClientUploadForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'  # Template para renderizar o formulário
    success_url = '/'  # Redireciona para a página inicial após salvar


@csrf_exempt  # Apenas para testes locais (use autenticação adequada em produção)
def upload_file(request, custom_link):
    # Localiza o cliente pelo link personalizado
    client = get_object_or_404(Client, custom_link=custom_link)

    if request.method == 'POST':
        form = ClientUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.client = client
            upload.save()
            return JsonResponse({'status': 'success', 'message': 'Arquivo enviado com sucesso!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    return render(request, 'upload.html', {'client': client})

def check_client_email(request):
    email = request.GET.get('email', '')
    
    try:
        # Valida o formato do e-mail
        validate_email(email)
        # Verifica se o e-mail já existe
        exists = Client.objects.filter(client_email__iexact=email).exists()
        return JsonResponse({
            'exists': exists,
            'valid': True
        })
    except ValidationError:
        return JsonResponse({
            'exists': False,
            'valid': False,
            'message': 'E-mail inválido'
        })
from django.views.generic import CreateView
from .models import Client, ClientUpload 
from .forms import ClientForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

AWS_ACCESS_KEY_ID = 'AKIAZ7SALK5PMRSG2BWC'
AWS_SECRET_ACCESS_KEY = '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'
AWS_BUCKET_NAME = 'falcon-aws-bucket'
AWS_REGION = 'sa-east-1' 

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'  # Template para renderizar o formulário
    success_url = '/'  # Redireciona para a página inicial após salvar

def upload_file_to_s3(file_obj, file_name):
    """
    Faz o upload de um arquivo para o bucket S3.
    """
    try:
        # Inicializa o cliente S3 com credenciais diretas
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        # Faz o upload do arquivo
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=file_obj)

        # Retorna a URL pública do arquivo
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        return file_url

    except NoCredentialsError:
        raise Exception("Erro: Credenciais da AWS não fornecidas ou inválidas.")
    except PartialCredentialsError:
        raise Exception("Erro: Credenciais incompletas fornecidas.")
    except Exception as e:
        raise Exception(f"Erro ao enviar o arquivo para o S3: {e}")


@csrf_exempt  # Apenas para testes locais; remova para produção ou use autenticação adequada
def upload_file(request, custom_link):
    """
    View para fazer upload de múltiplos arquivos de um cliente para o S3.
    """
    client = get_object_or_404(Client, custom_link=custom_link)

    if request.method == 'POST':
        print("Debug: request.FILES ->", request.FILES)  # Log de depuração
        files = request.FILES.getlist('files')  # Captura múltiplos arquivos
        if not files:
            return JsonResponse({'status': 'error', 'message': 'Nenhum arquivo enviado.'})

        uploaded_files = []
        for file in files:
            try:
                # Define o caminho do arquivo no bucket
                file_name = f"uploads/{client.client_name}/{file.name}"

                # Faz o upload do arquivo para o S3
                file_url = upload_file_to_s3(file.file, file_name)

                # Salva no banco de dados com uma referência ao arquivo
                upload = ClientUpload(client=client)
                upload.file.save(file.name, file)  # Salva o arquivo no modelo
                uploaded_files.append(file_url)

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        return JsonResponse({
            'status': 'success',
            'message': 'Arquivos enviados com sucesso!',
            'uploaded_files': uploaded_files  # URLs dos arquivos enviados
        })

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